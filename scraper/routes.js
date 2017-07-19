var router = require('express').Router();
var scraper = require('./scraper');


router.get('/start', function (req, res) {
    var before = scraper.running;
    scraper.start();
    var after = scraper.running;
    return res.json({ 
        before: before,
        after: after,
    });
});

router.get('/stop', function (req, res) {
    var before = scraper.running;
    scraper.stop();
    var after = scraper.running;
    return res.json({ 
        before: before,
        after: after,
    });
});

module.exports = router;