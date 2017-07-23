const redisClient = require('./redis');
const RUNNING_KEY = "SCRAPER_RUNNING";
const ON = "ON";
const OFF = "OFF";



class Scraper {
    constructor() {
        this.stop();
    }
    start() {
        return redisClient.getAsync(RUNNING_KEY).then(
            (val) => {
                console.log(val);
                if (val == ON) {
                    throw 'Already On';
                }
                return redisClient.setAsync(RUNNING_KEY, ON);
            }
        )
    }
    stop() {
        return redisClient.getAsync(RUNNING_KEY).then(
            (val) => {
                if (val == OFF) {
                    throw 'Already OFF';
                }
                return redisClient.setAsync(RUNNING_KEY, OFF);
            }
        )
    }
    append(val) {
        return redisClient.RPUSHAsync("LIST", val);
    }
    pop(val) {
        return redisClient.RPOPAsync("LIST");
    }
}

module.exports = new Scraper();