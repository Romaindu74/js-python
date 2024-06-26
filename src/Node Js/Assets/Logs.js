const {existsSync, mkdirSync, appendFileSync} = require("fs");

// Using module "kleur"
// Copyright (c) Luke Edwards <luke.edwards05@gmail.com> (lukeed.com)
class Colors {
    constructor() {
        let FORCE_COLOR, NODE_DISABLE_COLORS, NO_COLOR, TERM, isTTY = !0;
        "undefined" != typeof process && ({FORCE_COLOR, NODE_DISABLE_COLORS, NO_COLOR, TERM} = process.env || {},
        isTTY = process.stdout && process.stdout.isTTY),
        this.enabled = !NODE_DISABLE_COLORS && null == NO_COLOR && "dumb" !== TERM && (null != FORCE_COLOR && "0" !== FORCE_COLOR || isTTY)
    }
    init(x, y, txt) {
        var rgx = RegExp(`\\x1b\\[${y}m`, "g")
        , open = `\x1b[${x}m`
        , close = `\x1b[${y}m`;
        return this.enabled && null != txt ? open + (~("" + txt).indexOf(close) ? txt.replace(rgx, close + open) : txt) + close : txt
    }
    black   = txt => this.init(30, 39, txt);
    red     = txt => this.init(31, 39, txt);
    green   = txt => this.init(32, 39, txt);
    yellow  = txt => this.init(33, 39, txt);
    blue    = txt => this.init(34, 39, txt);
    magenta = txt => this.init(35, 39, txt);
    cyan    = txt => this.init(36, 39, txt);
    white   = txt => this.init(37, 39, txt);
    gray    = txt => this.init(90, 39, txt);
    grey    = txt => this.init(90, 39, txt);
}

class Logs {
    constructor() {
        this.path = process.cwd(),
        this.colors = new Colors();
    }

    /**
     * @param {Json} config 
     */
    setup(config) {
        "string" == typeof config.pathfile && (existsSync(this.path + "/" + config.pathfile) || mkdirSync(this.path + "/" + config.pathfile, {
            recursive: !0
        }),
        this.pf = config.pathfile),
        "string" == typeof config.formatfilename && (this.fn = config.formatfilename),
        "string" == typeof config.prefixlog && (this.pl = config.prefixlog)
    }

    /**
     * @param {Number} l 
     */
    gt(l) {
        return {
            5: {
                type: "CRITICAL",
                color: this.colors.red
            },
            4: {
                type: "ERROR",
                color: this.colors.red
            },
            3: {
                type: "WARNING",
                color: this.colors.yellow
            },
            2: {
                type: "INFO",
                color: this.colors.green
            },
            1: {
                type: "DEBUG",
                color: this.colors.white
            }
        }[l] || undefined
    }

    /**
     * @param {String} t 
     * @returns {String}
     */
    dt(t) {
        var formattedParts = (new Date).toLocaleString("fr-FR", {
            weekday: "long",
            year: "numeric",
            month: "2-digit",
            day: "2-digit",
            hour: "2-digit",
            minute: "2-digit"
        }).split(/[,\/\s:]+/);
        const tokenReplacements = [formattedParts[4], formattedParts[5], formattedParts[2], formattedParts[3], formattedParts[1]];
        return ["%h", "%m", "%j", "%M", "%a"].forEach((token,index)=>{
            t = t.replace(token, tokenReplacements[index])
        }
        ),
        t
    }

    /**
     * @param {String} t 
     */
    s(t) {
        var file = this.path;
        this.pf && (file += "/" + this.pf),
        this.fn ? file += "/" + this.dt(this.fn) : file += "Logs.txt",
        appendFileSync(file, t + `\n`, "utf8")
    }

    /**
     * @param {Number} l 
     * @param {String} t 
     */
    p(l, t) {
        var txt, level = this.gt(l);
        level && (txt = this.pl ? this.dt("" + this.pl + t) : t,
        1 < l) && this.s(txt.replace("%type", level.type))
        console.log(txt.replace('%type', level.color(level.type)));
    }

    /**
     * @param {String} text 
     */
    debug(...text) {
        this.p(1, text.join(" "))
    }

    /**
     * @param {String} text 
     */
    info(...text) {
        this.p(2, text.join(" "))
    }

    /**
     * @param {String} text 
     */
    warning(...text) {
        this.p(3, text.join(" "))
    }

    /**
     * @param {String} text 
     */
    error(...text) {
        this.p(4, text.join(" "))
    }

    /**
     * @param {String} text 
     */
    critical(...text) {
        this.p(5, text.join(" "))
    }
}

exports.Logs = Logs;