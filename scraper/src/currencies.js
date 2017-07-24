const plnx = require('plnx');
const fs = require('fs');


plnx.returnCurrencies(
    null,
    (err, data) => {
        let keys = Object.keys(data);
        for (var key in data){
            let item = data[key];
            if (!(item.disabled == 0 && item.delisted == 0 && item.frozen == 0)){
                delete data[key];
            }
        }
        data["length"] = Object.keys(data).length;
        console.log("Length is: " + data["length"]);
        fs.writeFile("currencies.json", JSON.stringify(data, null, 4), function (err) {
            if (err) {
                return console.log(err);
            }

            console.log("The file was saved!");
        });
    }
);
