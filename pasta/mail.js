// import { create, Client } from '@open-wa/wa-automate';
const wa = require('@open-wa/wa-automate');
const util = require('util') 
const { resolve } = require('path');


const TEXT = `Prezado(a),

Segue em anexo o extrato da comissão e o recibo de pagamento.

Atenciosamente,
Lincx Corretora`


const BROKERS_RECEIPTS_PATH = "/Users/cursedappleofsaggi/Documents/LINCX_BOT/pasta/"
const WHATSAPP_BOT_FILES_SENT_PATH = "/Users/cursedappleofsaggi/Documents/LINCX_BOT/pasta/wpp_files_sent.txt"


function save_file_as_sent(files) {
    const fs = require('fs');
    for (var i = 0; i < files.length; i++) {
        fs.appendFileSync(WHATSAPP_BOT_FILES_SENT_PATH, files[i] + '\n');
    }
    SENT_FILES++;
}


var SENT_FILES = 0


function start(client) {
    (async () => {
        var phoneAndFiles = JSON.parse(process.argv[2])
    
        for(var i = 0; i < phoneAndFiles.length; i++) {
            var obj = phoneAndFiles[i];
            await (async () => {
            console.log(`Sending to ${obj["Nome"]}'s Whatsapp. (${obj["Telefone"]})`)
            var chatId = `55${obj["Telefone"].replace(/ |-/g, "")}@c.us`;
        
            await client.sendText(chatId, TEXT)
            for(var j = 0; j < obj["Files To Be Send"].length; j++) {
                var file = `${BROKERS_RECEIPTS_PATH}${obj["Files To Be Send"][j]}`
                var filename = obj["Files To Be Send"][j].split('/')[1];
                await client.sendFile(chatId, file, filename);
                ;
            }
            save_file_as_sent(obj["Files To Be Send"])
            console.log('Done.')

            return new Promise(function(resolve, reject) {
                resolve(1)
            })
        })()
    }
    console.log(`\nFinished sending ${SENT_FILES} Whatsapp messages.`)
    process.exit(1)
})()
}


wa.create().then(client => start(client)).catch((e) => {});
