const express = require('express');
const sqlite3 = require('sqlite3').verbose();
const session = require('express-session');
const app = express();
const port = 3000;

app.use(express.static('public'));
app.use(express.urlencoded({ extended: true }));
app.set('view engine', 'ejs');

app.use(session({
  secret: 'your-secret-key',
  resave: false,
  saveUninitialized: true
}));

// Database setup
const db = new sqlite3.Database('./almuerzo.db', (err) => {
  if (err) {
    console.error(err.message);
  }
  console.log('Connected to the almuerzo database.');
});

db.serialize(() => {
  db.run("CREATE TABLE IF NOT EXISTS places (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, can_order BOOLEAN DEFAULT FALSE, can_sit BOOLEAN DEFAULT FALSE, can_takeaway BOOLEAN DEFAULT FALSE)");
  db.run("CREATE TABLE IF NOT EXISTS people (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, email TEXT, times_won INTEGER DEFAULT 0)");
  db.run("CREATE TABLE IF NOT EXISTS votes (place_id INTEGER, person_id INTEGER, FOREIGN KEY (place_id) REFERENCES places(id), FOREIGN KEY (person_id) REFERENCES people(id))");
  db.run("CREATE TABLE IF NOT EXISTS selections (id INTEGER PRIMARY KEY AUTOINCREMENT, place_id INTEGER, created DATETIME, FOREIGN KEY (place_id) REFERENCES places(id))");
});

// Routes
app.get('/', (req, res) => {
  const userid = req.query.userid;

  if (userid) {
    req.session.userset = userid;
    return res.redirect('/logged');
  }

  if (req.session.userset) {
    return res.redirect('/logged');
  }

  db.all("SELECT * FROM people ORDER BY name", [], (err, users) => {
    if (err) {
      console.error(err.message);
      return res.status(500).send('Server error');
    }
    res.render('homepage', { users: users });
  });
});

app.get('/logged', (req, res) => {
  const user_id = req.session.userset;

  if (!user_id) {
    return res.redirect('/');
  }

  db.get("SELECT * FROM people WHERE id = ?", [user_id], (err, user) => {
    if (err) {
      console.error(err.message);
      return res.status(500).send('Server error');
    }

    if (!user) {
      return res.redirect('/');
    }

    const now = new Date();
    const today_decision_time = new Date(now.getFullYear(), now.getMonth(), now.getDate(), 11, 30, 0, 0);
    const today_afternoon_time = new Date(now.getFullYear(), now.getMonth(), now.getDate(), 14, 30, 0, 0);

    const today_min = new Date(now.getFullYear(), now.getMonth(), now.getDate(), 0, 0, 0, 0);
    const today_max = new Date(now.getFullYear(), now.getMonth(), now.getDate(), 23, 59, 59, 999);

    db.all("SELECT selections.id, places.name FROM selections INNER JOIN places ON selections.place_id = places.id WHERE selections.created BETWEEN ? AND ?", [today_min.toISOString(), today_max.toISOString()], (err, todays_selection) => {
      if (err) {
        console.error(err.message);
        return res.status(500).send('Server error');
      }

      if (now > today_afternoon_time) {
        // end of day
        if (todays_selection.length > 0) {
          const place = todays_selection[0].name;
          return res.render('afternoon', { username: user.name, place: place });
        } else {
          return res.render('afternoon', { username: user.name, place: null });
        }
      } else if (todays_selection.length > 0) {
        // What was chosen
        const place = todays_selection[0].name;
        db.all("SELECT people.name FROM votes INNER JOIN people ON votes.person_id = people.id WHERE votes.created BETWEEN ? AND ?", [today_min.toISOString(), today_max.toISOString()], (err, people) => {
          if (err) {
            console.error(err.message);
            return res.render('lunch_chosen', { username: user.name, place: place, people: people });
          } else {
            return res.render('lunch_chosen', { username: user.name, place: null, people: people });
          }
        });
      } else {
        // vote time
        db.all("SELECT * FROM places ORDER BY RANDOM()", [], (err, places) => {
          if (err) {
            console.error(err.message);
            return res.status(500).send('Server error');
          }

          db.all("SELECT places.name FROM votes INNER JOIN places ON votes.place_id = places.id WHERE votes.created BETWEEN ? AND ? AND votes.person_id = ?", [today_min.toISOString(), today_max.toISOString(), user_id], (err, user_vote_today) => {
            if (err) {
              console.error(err.message);
              return res.status(500).send('Server error');
            }

            const already_voted = user_vote_today.length !== 0;
            let place_voted = null;

            if (already_voted) {
              place_voted = user_vote_today[0].name;
            }

            db.all("SELECT people.name FROM votes INNER JOIN people ON votes.person_id = people.id WHERE votes.created BETWEEN ? AND ?", [today_min.toISOString(), today_max.toISOString()], (err, all_votes_today) => {
              if (err) {
                console.error(err.message);
                return res.status(500).send('Server error');
              }
              return res.render('before_lunch', { username: user.name, places: places, voted: already_voted, voted_for: place_voted, votes_today: all_votes_today });
            });
          });
        });
      }
    });
  });
});

app.get('/chooseplace/:placeid', (req, res) => {
  const user_id = req.session.userset;
  const place_id = req.params.placeid;

  if (!user_id) {
    return res.redirect('/');
  }

  db.get("SELECT * FROM people WHERE id = ?", [user_id], (err, user) => {
    if (err) {
      console.error(err.message);
      return res.status(500).send('Server error');
    }

    if (!user) {
      return res.redirect('/');
    }

    db.get("SELECT * FROM places WHERE id = ?", [place_id], (err, place) => {
      if (err) {
        console.error(err.message);
        return res.status(500).send('Server error');
      }

      if (!place) {
        return res.status(404).send('Place not found');
      }

      const now = new Date();
      const today_min = new Date(now.getFullYear(), now.getMonth(), now.getDate(), 0, 0, 0, 0);
      const today_max = new Date(now.getFullYear(), now.getMonth(), now.getDate(), 23, 59, 59, 999);

      db.all("SELECT * FROM votes WHERE voter_id = ? AND created BETWEEN ? AND ?", [user_id, today_min.toISOString(), today_max.toISOString()], (err, votes_today) => {
        if (err) {
          console.error(err.message);
          return res.status(500).send('Server error');
        }

        const already_voted = votes_today.length !== 0;

        if (!already_voted) {
          db.run("INSERT INTO votes (place_id, person_id, created) VALUES (?, ?, ?)", [place_id, user_id, now.toISOString()], (err) => {
            if (err) {
              console.error(err.message);
              return res.status(500).send('Server error');
            }
            res.redirect('/logged');
          });
        } else {
          res.redirect('/logged');
        }
      });
    });
  });
});

app.get('/admin', (req, res) => {
  res.render('admin');
});

app.get('/admin/places', (req, res) => {
    db.all("SELECT * FROM places", [], (err, places) => {
        if (err) {
            console.error(err.message);
            return res.status(500).send('Server error');
        }
        res.render('admin_places', { places: places });
    });
});

app.post('/admin/places/add', (req, res) => {
    const name = req.body.name;
    db.run("INSERT INTO places (name) VALUES (?)", [name], (err) => {
        if (err) {
            console.error(err.message);
            return res.status(500).send('Server error');
        }
        db.all("SELECT * FROM places", [], (err, places) => {
            if (err) {
                console.error(err.message);
                return res.status(500).send('Server error');
            }
            res.render('admin_places', { places: places });
        });
    });
});

app.get('/admin/users', (req, res) => {
    db.all("SELECT * FROM people", [], (err, users) => {
        if (err) {
            console.error(err.message);
            return res.status(500).send('Server error');
        }
        res.render('admin_users', { users: users });
    });
});

app.post('/admin/users/add', (req, res) => {
    const name = req.body.name;
    const email = req.body.email;
    db.run("INSERT INTO people (name, email) VALUES (?, ?)", [name, email], (err) => {
        if (err) {
            console.error(err.message);
            return res.status(500).send('Server error');
        }
        db.all("SELECT * FROM people", [], (err, users) => {
            if (err) {
                console.error(err.message);
                return res.status(500).send('Server error');
            }
            res.render('admin_users', { users: users });
        });
    });
});

app.get('/signout', (req, res) => {
  delete req.session.userset;
  res.redirect('/');
});

// Start server
app.listen(port, () => {
  console.log(`Server listening on port ${port}`);
});
