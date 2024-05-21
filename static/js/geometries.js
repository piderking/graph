import * as THREE from "three";
import { TextGeometry } from './util/TextGeometrey.js'
import { FontLoader } from "./util/FontLoader.js"



const loader = new FontLoader();
const font_cache = []

const toRGBString(color){
    return `rgb(${color.r, color.g, color.b})`
} 
const loadFont = (url) => {
    let index = 0;
    const font = loader.load(
        // resource URL
        url,
    
        // onLoad callback
        function ( font ) {
            // do something with the font
            font_cache.push({
                font: font,
                index:  font_cache.length - 1,
                url: url,
            })
            index = index;
        },
    
        // onProgress callback
        function ( xhr ) {
            console.log( (xhr.loaded / xhr.total * 100) + '% loaded' );
        },
    
        // onError callback
        function ( err ) {
            console.log( 'An error happened' );
        }
    );
    console.log(font_cache[index])
    return font_cache[index] // Return List Element of the Index (newly created)
}
/**
 * Represents a 3D Box.
 * @constructor
 * @param {THREE.Scene} scene - THREE.JS Scene
 * @param {String} uuid - UUID of the Box Object in the graph system (not the mesh uuid)
 * @param {object} options - object containing the passed information on the object. All properties will be inherited from this object and if they're undefined then it will assign to place holder value
 */
export class Box{
    constructor(scene, uuid, options){
        
        this.scene = scene;
        this._alive = true;
        this.uuid = uuid

        // Undefined Checks
        options ??= {}
        options.scale ??= {x:1,y:1,z:1}
        options.position ??= {x:1,y:1,z:1}
        options.color ??= (Math.floor(Math.random() * 255), Math.floor(Math.random() * 255), Math.floor(Math.random() * 255)) 

        // Define based on options (object) parameter
        this.scale = options.scale
        this.position = options.position
        this.color = options.color


        // Define this.options (modify parameter before this)
        this.options = options

        
        // Geometric things
        this._geo = new THREE.BoxGeometry(this.scale.x, this.scale.y, this.scale.z);
        this._mat = new THREE.MeshBasicMaterial({
            color: new THREE.Color( toRGBString(this.color) )
        });
        
        // Manufacture Box Mesh
        this._mesh = new THREE.Mesh(this._geo, this._mat);
        
        // Set Position (Box Mesh scales are set in def)
        this._mesh.position.set(this.position.x, this.position.y, this.position.z);
    

        // Add to Scene
        this.scene.add(this._mesh)

        console.log(`Box Created of UUID: ${this.uuid}`)

    }
    object(){
        return this._mesh
    }
    move(x, y, z){
        this.position = {x: x, y: y, z:z}  
        this._mesh?.position.set(x, y, z);
    }
    is_alive(){
        return this._alive ?? false
    }
    remove(){
        this._geo.dispose();
        this._mat.dispose();
        this.scene.remove( this._mesh );
        this._alive = false
        console.log(`Box Removed of UUID: ${this.uuid}`)
    }

    getOptions(){
        return this.options
    }
}
export class Text{
    constructor(scene, uuid, text, options){
        // Assign Parameters
        this.scene = scene;
        this.text = text;
        this.uuid = uuid
        this._alive = true;

        // Auto Default if opp is Null
        options ??= {}
        options.scale ??= { x:1, y:1, z:1}
        options.position ??= { x:1, y:1, z:1}
        options.color ??= (Math.floor(Math.random() * 255), Math.floor(Math.random() * 255), Math.floor(Math.random() * 255))
        
        // Asign Options
        this.scale = options.scale
        this.position = options.position
        this.color = options.color
        this._url = options.url

        // Finish with Options
        this.options = options

        // Create URL and Font Object
        this._url ??= "fonts/lmk.json"
        this.font = () => {
            let font;

            font_cache.foreach((el)=>{
                if (el.url == this._url){
                    font = el.font
                }
            })
            // If undefined
            font ??= loadFont(this._url).font

            return inCache
        }
        // Text Options
        this.options.texto ??= {
            size: 80,
            depth: 5,
            curveSegments: 12,
            bevelEnabled: true,
            bevelThickness: 10,
            bevelSize: 8,
            bevelOffset: 0,
            bevelSegments: 5
        }
        
        // Geometric things
        this._geo = new TextGeometry( this.text, {
            font: this.font,
            size: this.options.texto.size,
            depth: this.options.texto.depth,
            curveSegments: this.options.texto.curveSegments,
            bevelEnabled: this.options.texto.bevelEnabled,
            bevelThickness: this.options.texto.bevelThickness,
            bevelSize: this.options.texto.bevelSize,
            bevelOffset: this.options.texto.bevelOffset,
            bevelSegments: this.options.text.bevelSegments
        } );
        this._mat = new THREE.MeshBasicMaterial({
            color: new THREE.Color(
                 toRGBString(this.color)
            )
        });
        this._mesh = new THREE.Mesh(this._geo, this._mat);
        
        // Position Geometry
        this._mesh.position.set(this.position.x, this.position.y, this.position.z);
        


        // Add to Scene
        this.scene.add(this._mesh)

        console.log(`Box Created of UUID: ${this.uuid}`)

    }
    object(){
        return this._mesh
    }
    move(x, y, z){
        this._mesh?.position.set(x, y, z);
    }
    
    remove(){
        this._geo.dispose();
        this._mat.dispose();
        this.scene.remove( this._mesh );
        this._alive = false;
        console.log(`Box Removed of UUID: ${this.uuid}`)
    }
}
export class Points{
    constructor(scene, uuid, points, options){

        // THREEjs Scene + Obj UUID
        this.scene = scene;
        this.uuid = uuid; 
        this.points = points
        this._alive = true;

        
        if (typeof(uuid) == undefined){
            console.error("UUID is undefined")
            alert("UUID is undefined") // developer mode
        }
        if (typeof(points) == undefined){
            console.error("Passed Points are UNDEFINED")
            alert("UUID is undefined") // developer mode
        }

        // Assign Static Variables if Variables passed are undefined
        options ??= {}
        options.scale ??= 1
        options.size ??= 1
        options.position ??= { x:1, y:1, z:1}
        options.color ??= (Math.floor(Math.random() * 255), Math.floor(Math.random() * 255), Math.floor(Math.random() * 255))
        
        // scale, position, points, color, size from options (modified) parameter
        this.color = options.color
        this.scale = options.scale
        this.position = options.position
        this.size = options.size


        this._mat =  new THREE.PointsMaterial({
            color: toRGBString(this.color)
        })
        this._mat.size = size
        this._mesh = new THREE.Points(
            new THREE.BufferGeometry().setAttribute("position", new THREE.BufferAttribute(
                new Float32Array( 
                    points
                ), 3
            )),
           this._mat
        )

        this._mesh.scale.set(scale, scale, scale)
        this._mesh.position.set(position.x, position.y, position.z)
        


        // Add to Scene
        this.scene.add(this._mesh)

        console.log(`Point Cloud Created of UUID: ${this.uuid}`)


    }
    object(){
        return this._mesh
    }
    move(x, y, z){
        this._mesh?.position.set(x, y, z);
    }
    
    remove(){
        //this._geo.dispose();
        //this._mat.dispose();
        this.scene.remove( this._mesh );
        this._alive = false;
        console.log(`Point Clouod Removed of UUID: ${this.uuid}`)
    }
    setSize(new_size){
        this.size = new_size
        this._mat.size = this.size

    }
    setColor(new_color){
        this.color = new_color
        this._mat.color = this.color

    }
}
