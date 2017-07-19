class Scraper {
    constructor(){
        this.running = false;
    }
    start() {
        this.running = true;
    }
    stop() {
        this.running = false;
    }
}

module.exports = new Scraper();