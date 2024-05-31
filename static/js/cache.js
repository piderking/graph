import { FontLoader } from "./util/FontLoader.js"

const loader = new FontLoader();


export class Cache{
    constructor(){
        this.font_cache = Array(0)
    }
    loadFont(url){
        this.downLoadFont(url)
    }
    downLoadFont(url){
        let index = 0;
        loader.load(
            // resource URL
            url,
        
            // onLoad callback
            function ( font ) {
                // do something with the font
                this.font_cache.push({
                    font: font,
                    index:  this.font_cache.length - 1,
                    url: url,
                })
                index = this.font_cache.length - 1;
    
            }.bind(this),
        
            // onProgress callback
            function ( xhr ) {
                console.log( (xhr.loaded / xhr.total * 100) + '% loaded' );
            },
        
            // onError callback
            function ( err ) {
                console.log( 'An error happened' );
            }
        );
    }
}