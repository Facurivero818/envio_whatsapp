const{image}= require("qr-image");
const {Client, LocalAuth, MessageMedia} = require('whatsapp-web.js');
//const qrcode = require('qrcode-terminal'); //Modulo para imprimir por consola el QR
const express = require('express');
const fs = require('fs');

const app = express();


app.use(express.json())

const client = new Client({
    authStrategy: new LocalAuth(),
    puppeteer: {
        headless: true,
        args: [
          "--disable-setuid-sandbox",
          "--unhandled-rejections=strict",
        ],
      },
});
client.initialize(); 

client.on('qr', (qr) => {
    client.estado = "ESCANEAR_QR";
    console.log(client.estado);
    //qrcode.generate(qr,{small:true});
    generateImage(qr);
});

client.on('ready', () => {
    client.estado = "LOGIN_SUCCESS";
    console.log(client.estado);
    console.log('Client is ready!');
});

client.on('disconnected',async (reason) => {
    client.estado = "DISCONNECT";
    console.log(client.estado);
    // client.destroy();
    await client.initialize();
});

//client.initialize(); 

//----------- Enviar Imagen-----------
const sendMedia = (phone,file)=>{
    try{
    const mediaFile = MessageMedia.fromFilePath(file);
    client.sendMessage(phone, mediaFile);
    }catch (error) {
        console.error("Error al enviar media:", error);
    }
}

//------------Enviar Mensaje --------------
const sendMsj= async (phone,message,file="")=>{

    if(client.estado =="LOGIN_SUCCESS"){
        var number = await client.isRegisteredUser(phone);//Verifico si el numero existe

        if(number){
            const response = await client.sendMessage(`${phone}@c.us`, message);//Envio mensaje mediante la libreria
            if(file !="") //Si viene una path, envio la imagen.
                sendMedia(`${phone}@c.us`,file);
            return { id: "Enviado correctamente"};//response.id.id
          }else
          {
          return { id: "Msj no enviado: Numero no registrado"}; 
        }
    }else{
        return {id: "LOGIN_FAIL"}
    }
}

//------------Generar Imangen SVG -----------
const generateImage = (base64) => {
    const path = `${process.cwd()}`;
    let qr_svg = image(base64, { type: "svg", margin: 4 });
    qr_svg.pipe(require("fs").createWriteStream(`${path}/qr.svg`));
}

//-----------Leer mensaje-------
const listenMsj=()=>{
    client.on('message',(msg)=>{
        const {from, to, body} = msg; //Guardo el num de telefo de quien lo mando, para quien y el msj
        //los números de telefonos vienen concatenados con "@c.us" al final
    })
}

//-----------Enviar Mensaje mediante API---------
const sendWithApi= async (req,res)=>{
    const { message, phone, image } = req.body;
    //console.log(message, phone, image); Para debuggear 
    const response = await sendMsj(phone,message,image);
    res.send(response) //{status: response}
}

const getStatus=(req,res)=>{
    const response = {
        "estado": client.estado
    }
    res.send(response);
}

app.post('/lead',sendWithApi);
app.post('/status',getStatus);
app.listen(3001,()=>{
    console.log('APP ESTA ARRIBA!');
})


