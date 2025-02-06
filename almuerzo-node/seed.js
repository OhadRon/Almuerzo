const sqlite3 = require('sqlite3').verbose();

const db = new sqlite3.Database('./almuerzo.db', (err) => {
  if (err) {
    console.error(err.message);
  }
  console.log('Connected to the almuerzo database.');
});

db.serialize(() => {
  db.run("INSERT INTO people (name, email) VALUES ('Alice', 'alice@example.com')");
  db.run("INSERT INTO people (name, email) VALUES ('Bob', 'bob@example.com')");
  db.run("INSERT INTO people (name, email) VALUES ('Charlie', 'charlie@example.com')");

  db.run("INSERT INTO places (name) VALUES ('The Italian Place')");
  db.run("INSERT INTO places (name) VALUES ('The Burger Joint')");
  db.run("INSERT INTO places (name) VALUES ('The Salad Bar')");
});

db.close((err) => {
  if (err) {
    console.error(err.message);
  }
  console.log('Closed the database connection.');
});
