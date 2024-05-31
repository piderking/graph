import * as THREE from "three";
import { TextGeometry } from './util/TextGeometrey.js'
import { FontLoader } from "./util/FontLoader.js"

const loader = new FontLoader();

const connections = [[3, 4], [0, 5], [17, 18], [0, 17], [13, 14], [13, 17], [18, 19], [5, 6], [5, 9], [14, 15], [0, 1], [9, 10], [1, 2], [9, 13], [10, 11], [19, 20], [6, 7], [15, 16], [2, 3], [11, 12], [7, 8]]
const toRGBString = (color) => {
    return new THREE.Color(color)
} 
async function syncFetch(url) {
    const response = await fetch(url);
    const text = await response.text();
    return text
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
        options.color ??= {r:Math.floor(Math.random() * 255), g:Math.floor(Math.random() * 255), b:Math.floor(Math.random() * 255)}

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
    
    constructor(scene, uuid, text, cache, options, font){
        // Assign Parameters
        this.scene = scene;
        this.cache = cache
        this.text = text;
        this.uuid = uuid
        this._alive = true;
        this.font ;
        // Auto Default if opp is Null
        options ??= {}
        options.scale ??= { x:1, y:1, z:1}
        options.position ??= { x:1, y:1, z:1}
        options.color ??= Math.floor(Math.random() * 10000) - 1
        
        // Asign Options
        this.scale = options.scale
        this.position = options.position
        this.color = options.color
        this._url = options.url

        // Finish with Options
        this.options = options

        // Create URL and Font Object
        this._url ??= "fonts/lmk.json"
        

        // Text Options
        this.options.texto ??= {
            size: 0.5,
            height: 0.1,
            depth:1,
            curveSegments: 13,
            bevelEnabled: true,
            bevelThickness: 0.001,
            bevelSize: 0.002,
            bevelOffset: 0,
            bevelSegments: 1
        }
   
        const json = JSON.parse( ); // you have to parse the data so it becomes a JS object 
        this.font = loader.parse(json)
    
        this._geo = new TextGeometry( this.text, {
            font: this.font,
            size: this.options.texto.size,
            depth: 1,
            curveSegments: this.options.texto.curveSegments,
            bevelEnabled: this.options.texto.bevelEnabled,
            bevelThickness: this.options.texto.bevelThickness,
            bevelSize: this.options.texto.bevelSize,
            bevelOffset: this.options.texto.bevelOffset,
            bevelSegments: this.options.texto.bevelSegments
        } );
        this._mat = new THREE.MeshBasicMaterial({
            color: new THREE.Color(
                toRGBString(this.color)
            )
        });
        this._mesh = new THREE.Mesh(this._geo, this._mat);
        
        // Position Geometry
        this._mesh.position.set(this.position.x, this.position.y, this.position.z);
        this._mesh.scale.set(this.scale.x, this.scale.y, this.scale.z);

        // Add to Scene
        this.scene.add(this._mesh)

        console.log(`Text Created of UUID: ${this.uuid}`)


    }
    
    object(){
        return this._mesh
    }
    move(x, y, z){
        this.position = {x, y, z}
        this._mesh?.position.set(x, y, z);

        this?.drawn_lines.forEach((el,)=>{
            el.geometry.translate(new THREE.Vector3(x, y, z))
        })
    }
    scale(x, y, z){
        alert("sdfs")
        this.scale = {x, y, z}
        this._mesh?.scale.set(x, y, z);

        this?.drawn_lines.forEach((el,)=>{
            el.geometry.scale(new THREE.Vector3(x, y, z))
        })
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
    constructor(scene, uuid, _points, options){
        this.points = []
        this.drawn_lines = []
        // THREEjs Scene + Obj UUID
        this.scene = scene;
        this.uuid = uuid; 
        this._alive = true;

        
        if (typeof(uuid) == undefined){
            console.error("UUID is undefined")
            alert("UUID is undefined") // developer mode
        }
        if (typeof(_points) == undefined){
            console.error("Passed Points are UNDEFINED")
            alert("UUID is undefined") // developer mode
        } 
        
        // Assign Static Variables if Variables passed are undefined
        options ??= {}
        options.scale ??= 1
        options.size ??= 1
        options.position ??= { x:1, y:1, z:1}
        options.color ??= 9001
        options.text ??= false
        options.lines ??= false

        
        
        // scale, position, points, color, size from options (modified) parameter
        this.color = options.color
        this.scale = options.scale
        this.position = options.position
        this.size = options.size
        this.lines = options.lines
        this.text = options.text


        this._mat =  new THREE.PointsMaterial({
            color: this.color
        })
        this._mat.size = this.size

        // Interpret Points
        _points.forEach((el, index, a)=>{
            if (index % 3 == 0){
                this.points.push( new THREE.Vector3(a[index]*this.scale.x+this.position.x, a[index+1]*this.scale.y+this.position.y, a[index+2]*this.scale.z+this.position.z))
            }
        })



        // Display Poitns
        this._geo = new THREE.BufferGeometry().setFromPoints(this.points)
        this._mesh = new THREE.Points(
            this._geo,
           this._mat
        )
        // Lines 
        //TODO Lines are not working, all data is here
        if (this.lines){
            connections.forEach((el, index)=>{
                
                let line = new THREE.LineSegments( 
                    new THREE.BufferGeometry().setFromPoints( [this.points[el[0]], this.points[el[1]]] ), 
                    new THREE.LineBasicMaterial({ color: 9001, 	linewidth: 4 })
                )
                //line.scale(this.scale.x, this.scale.y, this.scale.z)
                this.drawn_lines.push(line)
                this.scene.add(line)
            })
        } else {
            console.log("No Connection on Point CLoud: " + this.uuid)
        }

        //this._mesh.scale.set(this.scale.x, this.scale.y, this.scale.z, )
        //this._mesh.position.set(this.position.x, this.position.y, this.position.z)
        


        // Add to Scene
        this.scene.add(this._mesh)

        console.log(`Point Cloud Created of UUID: ${this.uuid}`)


    }
    object(){
        return this._mesh
    }
    move(x, y, z){
        this.position = {x, y, z}
        this._mesh?.position.set(x, y, z);

        this?.drawn_lines.forEach((el,)=>{
            el.geometry.translate(new THREE.Vector3(x, y, z))
        })
    }
    scale(x, y, z){
        this.scale = {x, y, z}
        this._mesh?.scale.set(x, y, z);

        this?.drawn_lines.forEach((el,)=>{
            el.geometry.scale(new THREE.Vector3(x, y, z))
        })
    }
    
    remove(){

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
