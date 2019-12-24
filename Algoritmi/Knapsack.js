export default class Knapsack{
    P=[];
    J=[];
    cryptedText="";
    decryptedText="";    n=-1;m=-1;
    constructor(){
        this.P = [2,3,7,14,30,57,120,251];
        this.n = 491;
        this.m=41;
        this.im=-1;
        this.calculateVectorJ();
        this.calculateM();
    }
    getCryptedText(){
        return this.cryptedText;
    }
    getDecryptedText(){
        return this.decryptedText;
    }
    calculateVectorJ(){
        for(var i= 0;i<this.P.length;i++){
            this.J[i]=(this.P[i]*this.m) % this.n;
        }
    }
    calculateM(){
        var nadjen= false;
        while(!nadjen){
            if((this.m*this.im) % this.n == 1){
                nadjen = true;
            }else{
                this.im++;
            }
        }
    }
    crypt(text){
        for(var i= 0;i<text.length;i++){
            var C=0;
            var binOfChar = text.charCodeAt(i).toString(2);
            if(binOfChar.length!=8){
                var dodatak = 8-binOfChar.length;
                for(var j= 0; j<dodatak; j++){
                    binOfChar = "0"+binOfChar;
                }
            }
            for(var j= 0;j<8;j++){
                C+=this.J[j]*binOfChar.charAt(j);
            }
            this.cryptedText = this.cryptedText.concat(C.toString());
            if(i!= text.length-1){
                this.cryptedText = this.cryptedText.concat(",")
            }
        }
    }
    decrypt(text){
        var pomocna = text.split(",");
        for(var i= 0;i<pomocna.length;i++){
            var TC = (parseInt(pomocna[i])*this.im)%this.n;
            var result="";
            for(var j=this.P.length-1;j>-1;j--){
                if(TC/this.P[j] >= 1){
                    result = "1"+result;
                    TC = TC - this.P[j];
                }else{
                    result = "0"+result;
                }
            }
            if(TC!=0){
                console.log("Greska");
            }
            this.decryptedText = this.decryptedText.concat(String.fromCharCode(parseInt(result, 2)));
        }
    }
}