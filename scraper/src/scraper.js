const redis = require("redis");
const client = redis.createClient(process.env.REDIS_PORT, process.env.REDIS_HOST);
const wsServer = require('./ws-server');
const RUNNING_KEY = "SCRAPER_RUNNING"
const ON = "ON"
const OFF = "OFF"


class Scraper {
    constructor(){
        this.stop();
    }
    start(successcb, errorcb) {
        client.get(RUNNING_KEY, (err, reply) => {
            if (reply == ON){
                errorcb && errorcb("Already on");
                return;
            }
            client.set(RUNNING_KEY, ON, function(err, reply){
                if (err){
                    errorcb && errorcb(err);
                    return;
                }
                successcb && successcb();
            });
        });
    }
    stop(successcb, errorcb) {
        client.get(RUNNING_KEY, (err, reply) => {
            if (err){
                errorcb && errorcb(err);
                return;
            }
            if (reply != ON){
                errorcb && errorcb("Already off");
                return;
            }
            client.set(RUNNING_KEY, OFF, function(err, reply){
                if (err){
                    errorcb && errorcb(err);
                    return;
                }
                successcb && successcb();
            })
        });
    }
}

module.exports = new Scraper();