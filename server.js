const express = require('express');
const mongoose = require('mongoose');

const app = express();

const dbURI = 'mongodb+srv://<db_username>:<db_password>@<db_cluster>/<db_name>?retryWrites=true&w=majority';
const options = {
  useNewUrlParser: true,
  useUnifiedTopology: true,
};

mongoose.connect(dbURI, options)
  .then(() => {
    console.log('Connected to MongoDB');
  })
  .catch((error) => {
    console.error('Error connecting to MongoDB:', error);
  });

app.use(express.json());

app.get('/api/users', (req, res) => {
    // Handle GET request for retrieving users
});
  
app.post('/api/users', (req, res) => {
    // Handle POST request for creating a new user
});
  
const port = 3000;
app.listen(port, () => {
    console.log(`Server listening on port ${port}`);
});
  