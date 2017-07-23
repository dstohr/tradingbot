var router = require('express').Router();
var scraper = require('./scraper');


router.get('/start', function (req, res) {
    scraper.start()
        .then(() => { res.send({ msg: "OK" }) })
        .catch((err) => { res.send({ msg: err }) });
});

router.get('/stop', function (req, res) {
    scraper.stop()
        .then(() => { res.send({ msg: "OK" }) })
        .catch((err) => { res.send({ msg: err }) });
});

router.get('/append', function (req, res) {
    scraper.append("lalal")
        .then(() => { res.send({ msg: "OK" }) })
        .catch((err) => { res.send({ msg: err }) });
});

router.get('/pop', function (req, res) {
    scraper.pop()
        .then((val) => { res.send({ msg: val }) })
        .catch((err) => { res.send({ msg: err }) });
});

module.exports = router;