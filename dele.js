var fs = require("fs");
var getFolderSize = path => {
    var size = 0;
    if (fs.existsSync(path)) {
        fs.readdirSync(path).forEach(function(file, index) {
            var curPath = path + "/" + file;
            var states = fs.statSync(curPath);
            if (!states.isDirectory()) {
                size += states.size;
            } else {
                size += 100000000000;
            }
        });
    }
    return size;
};

var deleteFolderRecursive = function(path) {
    if (fs.existsSync(path)) {
        fs.readdirSync(path).forEach(function(file, index) {
            var curPath = path + "/" + file;
            if (fs.lstatSync(curPath).isDirectory()) {
                // recurse
                deleteFolderRecursive(curPath);
            } else {
                // delete file
                fs.unlinkSync(curPath);
            }
        });
        fs.rmdirSync(path);
    }
};

var deleteFolder = function(path, size = 100000000) {
    if (fs.existsSync(path)) {
        fs.readdirSync(path).forEach(function(file, index) {
            var curPath = path + "/" + file;
            var states = fs.statSync(curPath);
            if (states.isDirectory()) {
                let currentSize = getFolderSize(curPath);
                if (currentSize < size) {
                    console.log(curPath);
                    deleteFolderRecursive(curPath);
                }
            }
        });
    }
};

deleteFolder("E:/Download/other/11");
deleteFolder("F:/电影/movies");
