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

app.use(function (req, res, next) {
    var err = new Error('Not Found');
    err.status = 404;
    next(err);
});

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

app.use(function (err, req, res, next) {
    res.status(err.status || 500);
    res.json({
        'errors': {
            message: err.message,
            error: {}
        }
    });
});

const server = app.listen(process.env.PORT || 3000, function () {
    console.log('Listening on port ' + server.address().port);
});