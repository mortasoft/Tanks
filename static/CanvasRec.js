var width = 336;
var height = 324;
var pixWidth = 28;
var pixHeight = 27;
var canvas = document.getElementById('canvas');
var ctx = canvas.getContext('2d');
var local=false;

Tank = function(x, y) {
    this.x = x;
    this.y = y;
    this.hp = 100;
    this.direction= "";
    this.up =  new Image();
    this.up.src = "static/tank1D_up.png";
    this.down= new Image();
    this.down.src ="static/tank1D_down.png";
    this.left= new Image();
    this.left.src = "static/tank1D_left.png";
    this.right= new Image();
    this.right.src = "static/tank1D_right.png";

try {
    if (this.up.complete) {
    ctx.drawImage(this.right, 0, 0);
} else {
    this.up.onload = function () {
        ctx.drawImage(this.right, 0, 0);
    };
}
}
catch(err) {
    console.log(err);
}

}



var tanque1 = new Tank(10,10);

