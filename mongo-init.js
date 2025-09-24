// mongo-init.js
db = db.getSiblingDB('visualization_db');

db.createUser({
  user: 'admin',
  pwd: 'admin123',
  roles: [
    {
      role: 'readWrite',
      db: 'visualization_db'
    }
  ]
});