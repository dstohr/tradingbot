const express = require('express'),
    cors = require('cors'),
    errorhandler = require('errorhandler')

const isProduction = process.env.MODE === 'PRODUCTION';

const app = express();

app.use(cors());
app.use(require('morgan')('dev'));

if (!isProduction) {
    app.use(errorhandler());
}

app.use(require('./routes'));

if (!isProduction) {
    app.use(function (err, req, res, next) {
        console.log(err.stack);

        res.status(err.status || 500);

        res.json({
            'errors': {
                message: err.message,
                error: err
            }
        });
    });
}

require('./db').connect()
require('./ws-server');

const server = app.listen(process.env.PORT || 3000, function () {
    console.log('Listening on port ' + server.address().port);
});