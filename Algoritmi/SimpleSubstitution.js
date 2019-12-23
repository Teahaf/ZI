export default class SimpleSubstitution {
    result ="";
    resultDec="";
    initializationVector = "";
    constructor(){
        this.initializationVector = "s";
    }

    crypt(text) {
        var map = this.rotateMap(false);
        return text.split('').map(function(v) {// Replace character by value
            if(v.charCodeAt(0)<=90 && v.charCodeAt(0)>=65 ){
                return map[v.toLowerCase()].toUpperCase();
            }else if(v.charCodeAt(0)>=97 && v.charCodeAt(0)<=122){
                return map[v];
            }else{
                return v;
            }
        }).join("");
    }

    decrypt(text){
        var map = this.rotateMap(true);
        return text.split('').map(function(v) {// Replace character by value
            if(v.charCodeAt(0)<=90 && v.charCodeAt(0)>=65 ){
                return map[v.toLowerCase()].toUpperCase();
            }else if(v.charCodeAt(0)>=97 && v.charCodeAt(0)<=122){
                return map[v];
            }else{
                return v;
            }
        }).join("");
    }

    cryptChar(v){
        var map = this.rotateMap(false);
        return map[v.toLowerCase()];
    }
    decryptChar(v){
        var map = this.rotateMap(true);
        return map[v.toLowerCase()];
    }

    rotateMap(decrypt){
        var map = {
            a: 'q', b: 'w', c: 'e',
            d: 'r', e: 't', f: 'y',
            g: 'u', h: 'i', i: 'o',
            j: 'p', k: 'a', l: 's',
            m: 'd', n: 'f', o: 'g',
            p: 'h', q: 'j', r: 'k',
            s: 'l', t: 'z', u: 'x',
            v: 'c', w: 'v', x: 'b',
            y: 'n', z: 'm', " ": ' ',
            ".":"?"
        };
        if(decrypt){
            map = (function() {
                var tmp = {};
                var k;
                // Populate the tmp variable
                for(k in map) {
                    if(!map.hasOwnProperty(k)) continue;
                    tmp[map[k]] = k;
                }
                return tmp;
            })();
        }
        return map;
    }
    pcbcCrypt(text){
        var funcres = this.calacIV(text, this.initializationVector);
        this.result = this.result.concat(funcres.first);
        for(var i=1;i<text.length;i++){
            var inFunc =this.calacIV(text.slice(i),funcres.second);
            funcres.second  = inFunc.second;
            this.result = this.result.concat(inFunc.first);
        } 
        console.log( this.result);
    }

    calacIV(text, initializationVector){    
        var temp="";
        for(var i=0; i< text.charCodeAt(0).toString(2).length; i++){
            temp = temp.concat(text.charCodeAt(0).toString(2).charAt(i)^initializationVector.charCodeAt(0).toString(2).charAt(i));
        }
        var index = 65 +(parseInt(temp, 2) % 26);
        var xoredChar = String.fromCharCode(index);
        var trying = this.cryptChar(xoredChar);
        var nextInVector = "";
        for(var i=0; i< text.charCodeAt(0).toString(2).length; i++){
            nextInVector = nextInVector.concat(text.charCodeAt(0).toString(2).charAt(i)^trying.charCodeAt(0).toString(2).charAt(i));
        }
        return {first: trying, second: nextInVector};
    }

    pcbcDecrypt(text){
        var resultFunc = this.calcDecVI(text, this.initializationVector);
        this.resultDec = this.resultDec.concat(resultFunc.first);
        for(var i=1;i<text.length;i++){
            var inFunc =this.calcDecVI(text.slice(i),resultFunc.second);
            resultFunc.second  = inFunc.second;
            this.resultDec = this.resultDec.concat(inFunc.first);
        }
        console.log(this.resultDec);
    }
    calcDecVI(text, initializationVector){
        var slovo = this.decryptChar(text.charAt(0));
        var temp = "";
        for(var i=0; i< slovo.charCodeAt(0).toString(2).length; i++){
            temp = temp.concat(slovo.charCodeAt(0).toString(2).charAt(i)^initializationVector.charCodeAt(0).toString(2).charAt(i));
        }
        var index = 65 +(parseInt(temp, 2) % 26);
        var resultChar = String.fromCharCode(index);
        this.resultDec = this.resultDec.concat(resultChar);
        var nextInVector="";
        for(var i=0; i< text.charCodeAt(0).toString(2).length; i++){
            nextInVector = nextInVector.concat(text.charCodeAt(0).toString(2).charAt(i)^resultChar.charCodeAt(0).toString(2).charAt(i));
        }
        return {
            first: resultChar,
            second: nextInVector
        };
    }
}

var ss = new SimpleSubstitution();
var text ="mihajlo VOLI da jede govna 2345678i9<>>>><>!@#$%^Y&U*I(O|'["
var crtext = ss.crypt(text);
console.log(crtext);
console.log(ss.decrypt(crtext));

