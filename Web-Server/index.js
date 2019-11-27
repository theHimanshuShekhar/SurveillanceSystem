const express = require('express')
const fs = require('fs')
var cors = require('cors');



const app = express()
const port = 3000


// Set up a whitelist and check against it:
var whitelist = ['http://localhost:4200', 'http://example2.com']
var corsOptions = {
    origin: function (origin, callback) {
        if (whitelist.indexOf(origin) !== -1) {
            callback(null, true)
        } else {
            callback(new Error('Not allowed by CORS'))
        }
    }
}

// Then pass them to cors:
app.use(cors(corsOptions));

app.get('/', (request, response) => {
    response.send('Server Online at Port: ' + port)
})


app.get('/folders', (req, res) => {
    const results = {
        test: 'Successfull'
    };
    const folders = fs.readdirSync('../results');
    res.json(results);
});

app.listen(port, (err) => {
    if (err) {
        return console.log('something bad happened', err)
    }

    console.log(`server is listening on ${port}`)
})