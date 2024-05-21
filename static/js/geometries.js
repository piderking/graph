import * as THREE from "three";
import { TextGeometry } from './util/TextGeometrey.js'
import { FontLoader } from "./util/FontLoader.js"
/**
 * Represents a 3D Box.
 * @constructor
 * @param {THREE.Scene} scene - THREE.JS Scene
 * @param {object} scale - x, y, z of the scale, default to 1
 * @param {object} position - x, y, z of the box, default to 
 */


const loader = new FontLoader();

const loadFont = (url) => {
    let lFont;
    const font = loader.load(
        // resource URL
        url,
    
        // onLoad callback
        function ( font ) {
            // do something with the font
            console.log( font );
            lFont = font
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
    console.log(lFont)
    return lFont
}
export class Box{
    constructor(scene, uuid, scale, position, color){
        this.scene = scene;
        this.scale = scale
        this.position = position
        this.color = color
        // Geometric things
        this._geo = new THREE.BoxGeometry(scale.x, scale.y, scale.z);
        this._mat = new THREE.MeshBasicMaterial({
            color: this.color
        });
        this._mesh = new THREE.Mesh(this._geo, this._mat);
        
        this._mesh.position.set(position.x, position.y, position.z);
        
        // Set ID
        this.uuid = uuid
        //this._mesh.uuid = uuid;

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
        console.log(`Box Removed of UUID: ${this.uuid}`)
    }
}
export class Text{
    constructor(scene, uuid, text, options){
        // Assign Parameters
        this.scene = scene;
        this.text = text;
        this.uuid = uuid

        // Asign Options
        this.scale = options.scale
        this.position = options.position
        this.color = options.color
        this._url = options.url

        // Finish with Options
        this.options = options

        // Auto Default if opp is Null
        this.scale ??= { x:1, y:1, z:1}
        this.position ??= { x:1, y:1, z:1}
        this.color ??= `rgb(${Math.floor(Math.random() * 255)}, ${Math.floor(Math.random() * 255)}, ${Math.floor(Math.random() * 255)})`
        this._url ??= "fonts/lmk.json"
        this.font = loadFont(
            this._url
        )
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
                this.color
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
        console.log(`Box Removed of UUID: ${this.uuid}`)
    }
}
export class Points{
    setSize(new_size){
        this.size = new_size
        this._mat.size = this.size

    }
    setColor(new_color){
        this.color = new_color
        this._mat.color = this.color

    }
    constructor(scene, uuid, scale, position, points, color, size){
        this.color = color
        this.scene = scene;
        this.scale = scale
        this.position = position
        this.size = size


        this._mat =  new THREE.PointsMaterial({
            color: this.color
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
        
        // Set ID and set meshes ID to it
        this.uuid = uuid;

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
        console.log(`Point Clouod Removed of UUID: ${this.uuid}`)
    }
}