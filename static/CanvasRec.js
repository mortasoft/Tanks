var width = 1366;
var height = 768;
var pix = 28;
var pixWidth = 28;
var pixHeight = 27;
var canvas = document.getElementById('canvas');
var ctx = canvas.getContext('2d');
var tanks = [];
var time= 500;

Tank = function(x, y, direction) {
    this.x = x;
    this.y = y;
    this.hp = 100;
    this.direction= "";
    this.image =  document.createElement("img");
    switch(direction){
        case 'left':
            this.image.src = "static/tank1D_left.png";
            break;
        case 'right':
            this.image.src = "static/tank1D_right.png";
            break;
        case 'up':
            this.image.src = "static/tank1D_up.png";
            break;
        case 'down':
            this.image.src = "static/tank1D_down.png";
            break;
    }
    
    var parent = this;
    this.image.onload=function(){
       ctx.drawImage(parent.image,parent.x,parent.y);
    }

    this.rotate = function (x,y,degrees) {

   // ctx.clearRect(this.x,this.y,pix,pix);
   // ctx.save();
    ////ctx.translate(x,y);
    ctx.rotate(degrees*Math.PI/6);
   // ctx.drawImage(this.image,this.x,this.y);
    };

    this.move = function (x,y,direction) {
        ctx.clearRect(parent.x, parent.y, pix, pix);
        parent.x = x;
        parent.y = y;
        parent.direction = direction;
        ctx.drawImage(parent.image,parent.x,parent.y);
    }}

function createNewTank() {
    $.ajax({
        type: "GET",
        url: "http://127.0.0.1:8888/createTank",
        async: false,
        success: function(data) {
            console.log("Se creo el tanque")
        }
    });
}

function createAllTanks(){
 $.ajax({
        type: "GET",
        url: "http://127.0.0.1:8888/tanks",
        async: false,
        success: function(data) {
            for (var i = 0; i < data.length; i++) {
                var tank = data[i];
                if(tank.alive==true){
                    aNewTank = new Tank( tank.x, tank.y);
                    tanks.push(aNewTank);
                }

                console.log(tank.alive);
                 
            }
        }
        });
}

function play(){
 $.ajax({
        type: "GET",
        url: "http://127.0.0.1:8888/play",
        async: false,
        success: function(data) {
            ctx.clearRect(0,0,width,height);
            for (var i = 0; i < data.length; i++) {
                var tank = data[i];
                if(tank.alive==true){
                    aNewTank = new Tank( tank.x, tank.y,tank.direction);
                    tanks.push(aNewTank);
                }
            }
        }
         // Fin Ajax
    });
}

createNewTank();

$(document).ready(function() { setInterval(function() {play() ;}, time);
});