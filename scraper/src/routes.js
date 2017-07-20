var router = require('express').Router();
var scraper = require('./scraper');


router.get('/start', function (req, res) {
    scraper.start(
        ()=>{
            res.send({msg: "OK"});
        },
        (msg)=>{
            res.send({msg: msg});
        }
    );
});

router.get('/stop', function (req, res) {
    scraper.stop(
        ()=>{
            res.send({msg: "OK"});
        },
        (msg)=>{
            res.send({msg: msg});
        }
    );
});

module.exports = router;