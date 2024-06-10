function Table(options) {
    let result = "";

    result += "+";
    for (let width = 0; width < options.width - 2; width++) {
        result += "-";
    }
    result += "+\n";

    for (let key in options.data) {
        let maxwidth = Math.floor((options.width - 4) / 2);

        let Key = key.length > maxwidth ? (key.substring(0, maxwidth - 4) + "...") : key;
        result += `| ${Key}`;
        for (let width = 0; width < maxwidth - Key.length; width++) {
            result += " ";
        }

        let Values = options.data[key];
        for (let i = 0; i < Values.length; i++) {
            let Text = options.data[key][i];
            if (Text == true) {
                Text = "";
                for (let j = 0; j < maxwidth - 1; j++) {
                    Text += "-";
                }
            }
            result += `| ${Text.length > maxwidth ? (Text.substring(0, maxwidth - 4) + "...") : Text}`;
            for (let width = 0; width < maxwidth - `${Text}`.length - 1; width++) {
                result += " ";
            }
            if (i != Values.length - 1) {
                result += "|\n|";
                for (let width = 0; width < maxwidth + 1; width++) {
                    result += " ";
                }
            }
        }
        result += "|\n";
    }

    result += "+";
    for (let width = 0; width < options.width - 2; width++) {
        result += "-";
    }
    result += "+\n"

    return result;
}

function cwd(path = __filename) {
    let file = path.split('/').join('\\').split('\\');
    file.pop();
    return file.join('/') + '/';
}

exports.Table = Table;
exports.cwd   = cwd;