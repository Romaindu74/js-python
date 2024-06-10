const ws = require("ws");
const fs = require("fs");

const { Encrypt, Decrypt } = require("./Libs/Js/aes");
const { Deflate, Inflate } = require("./Libs/Js/zlib");

const { Logs }             = require("./Assets/Logs");
const { Table, cwd }       = require("./Assets/Libs");

globalThis.Log = new Logs();

Log.setup({
    pathfile: 'Logs',
    formatfilename: 'Log %j-%M-%a.log',
    prefixlog: '[%h:%m %j/%M/%a][%type] '
});

class Client {
    /**
     * @param {string} uuid 
     * @param {ws} ws 
     * @param {Server} server 
     */
    constructor(uuid, ws, server) {

        this.server = server;
        this.uuid   = uuid;
        this.ws     = ws;

        this.client_uuid = "";

        ws.on("message", message => {
            this.onMessage(message.toString());
        })

        ws.on("close", () => {
            delete this.server.Clients[this.client_uuid];
        })

        setInterval(() => {
            this.send(``, false, "info");
        }, 1000)
    };

    /**
     * @param {string} Message
     */
    onMessage(Message) {
        let data = this.server.secure.decrypt_data(Message);

        if (data.type == "info") {
            this.client_uuid = data.data.uuid;
            this.server.Clients[data.data.uuid] = data.data
        } else if (data.type == "ping") {
            this.send(data.data, false, "ping");
        }
    }

    send(Message, reponse = false, type = "message") {
        this.ws.send(this.server.prepare_data(Message, reponse, type)[0]);
    }
}

class Secure {
    /**
     * @param {Server} server 
     */
    constructor(server) {
        this.server = server;
        
        this.def_receive = {
            "zlib": [
                Inflate
            ],
            "aes": [
                Decrypt
            ]
        };
    
        this.def_key = this.def_receive;
    
        this.def_send = {
            "zlib": [
                Deflate
            ],
            "aes": [
                Encrypt
            ]
        };

        this.gen_key = this.def_send;
    }
    
    /**
     * @param {number} length 
     * @returns {string}
     */
    generateSecurityKey = (length = 128) => {return Array.from({length}, () => 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'.charAt(Math.floor(Math.random() * 62))).join('')}

    /**
     * @param {String} key 
     * @returns {string}
     */
    genKey(key) {
        let result = JSON.stringify({
            method: "zlib-aes-zlib",
            key: this.generateSecurityKey(1024)
        });

        for (let method of ["zlib", "aes"]) {
            result  = this.gen_key[method][0](result, key);
        }

        let path = `${this.server.path}Key`;
        let date = new Date().toISOString().split("T")[0];

        if (!fs.existsSync(path)) {
            fs.mkdirSync(path);
        }

        fs.writeFileSync(`${path}/Key ${date}.key`, result);

        return `${path}/Key ${date}.key`;
    }

    /**
     * @param {string} file 
     * @param {string} key 
     */
    setKey(file, key) {
        let result  = file;

        for (let method of ["aes", "zlib"]) {
            result  = this.def_key[method][0](result, key);
        }
        
        let ops     = JSON.parse(result);

        this.keyset = true;

        this.method = ops['method'];
        this.key    = ops['key'];
    }

    /**
     * @param {string} data 
     * @returns {object}
     */
    decrypt_data(data) {
        let result = data;
    
        for (let method of this.method.split("-").reverse()) {
            for (let func of this.def_receive[method]) {
                result = func(result, this.key);
            }
        }
    
        return JSON.parse(result);
    }
    
    /**
     * @param {Object} data 
     * @returns {String}
     */
    encrypt_data(data) {
        let result = JSON.stringify(data);
    
        for (let method of this.method.split("-")) {
            for (let func of this.def_send[method]) {
                result = func(result, this.key);
            }
        }
    
        return result;
    }
}

class Info {
    /**
     * @returns {number}
     */
    get get_time() {
        return Math.floor(Date.now() / 1000);
    }

    /**
     * @param {number} start 
     * @param {string} format 
     */
    time(start, format = "%S") {
        let startTime = this.get_time - start;

        let replace = {
            "%S": startTime,
            "%H": parseInt(startTime / 3600),
            "%m": parseInt(startTime / 60)   % 60,
            "%s": startTime          % 60
        }
        let result = format;
        for (let replacer of Object.keys(replace)) {
            result = result.replace(replacer, replace[replacer]);
        }

        return result;
    }
}

class Server {
    /**
     * @param {object} options 
     */
    constructor(options = {}) {
        if (Object.keys(options).length === 0) {

        }

        if (options.server && options.port) {

        }

        this.Clients = {};
        this.options = options;

        this.mid     = 0;

        this.path    = cwd(__filename);

        this.info   = new Info();
        this.secure = new Secure(this);
    }

    uuid() {
        return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g,
            c => (
                (c == 'x' ? Math.random() * 16 : (Math.random() * 16 & 0x3 | 0x8)) | 0
            ).toString(16)
        );
    }

    run() {
        this.ws = new ws.Server(this.options);

        this.ws.on("connection", client => {
            let uuid = this.uuid();

            new Client(uuid, client, this);
        })

        setInterval(() => {
            console.clear();

            console.log(this.Log());
        }, 1000);
    }

    /**
     * @param {string} file_path 
     * @param {string} key 
     */
    set_key(file_path, key) {
        this.key_path = file_path;
        this.key      = key;

        if (!fs.existsSync(this.key_path)) {
            this.key_path = this.secure.genKey(this.key);
        }

        this.secure.setKey(fs.readFileSync(this.key_path, "utf-8"), this.key);
    }

    Log(width = 100) {
        let result = {
            width: width,
            data: {
                Clients: [
                    `${Object.keys(this.Clients).length} clients.`,
                    ``
                ]
            }
        };

        for (let i = 0; i < Object.keys(this.Clients).length; i++) {
            let client = Object.values(this.Clients)[i];

            let _ping = (typeof client.ping == "undefined" ? ["inf"] : client.ping), ping = _ping[_ping.length - 1];

            result.data[`Client ${i}`] = [
                true,
                `Name: ${client.name}`,
                `uuid: ${client.uuid}`,
                '',
                `Send: ${(client.recv_char * 8) / 1000} Ko`,
                `Received: ${(client.send_char * 8) / 1000} Ko`,
                '',
                `Ping: ${(typeof ping == "number" ? ping.toFixed(2) : ping)}ms`,
                '',
                `Started: ${this.info.time(client.start_time, "%HHeure, %mminutes")}`
            ]
        }

        return Table(result);
    }

    /**
     * @returns {number}
     */
    get get_mid() {
        this.mid += 1;

        return this.mid;
    }

    prepare_data(data, reponse = false, type = "message") {
        const mid = this.get_mid;
    
        return [
            this.secure.encrypt_data({
                timestamp: this.info.get_time,
                mid: mid,
                type: type,
                data: data,
                reponse: reponse
            }),
            mid
        ];
    }
}

let Main = new Server({
    port: 8765
});

Log.info("Set Key");
Main.set_key("./Key/Test.key", "salut-e ?");

Main.run();