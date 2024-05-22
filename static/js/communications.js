import * as THREE from "three";
import {Box, Points} from "./geometries.js"
export class Communications {

    constructor(scene){
        this.userDefinedCallbacks = {}
        this.scene = scene
        this.synced = false
        this.objects = []
        this.socket = io("/", {
          reconnectionDelayMax: 10000,
          auth: {
            token: ""
          },
          query: {
            "my-key": "my-value"
          }
        });
        

        this.initSocketConnection()
 
        

    }
    initSocketConnection() {
      
      console.log("Initializing socket.io...");
      this.socket.on("connect", () => {
        console.log("My socket ID:", this.socket.id);
      });
      console.log("SocketIO Initalized... Informing")
      this.socket.emit("init", {}) // No Objects saved locally yet
      
      console.log("Trying to Sync Data")
      this.socket.on("sync", (data)=>{
        if (this.synced){
          console.error("Already Synced")
          return
        }
        this.synced = true // So more syncs can't accidenatally be sent
        console.log("Starting Sync of Data")
        console.log(`Amount of objects to sync: ${data.len}`)
        console.log(`Client SID: ${data.sid}... Matches: ${"True" ? data.sid == this.socket.id : "False"}`)
        console.log(data.objects)
        const objects = data.objects
        // TODO Add Objects Here (Assume Everything is being added)
        
        objects.forEach((object) => {
          switch (object.type){
            case "box":
              this.addBox(object.uuid, object.scale, object.position, object.color)
            case "point cloud":
              console.log(object)
              this.addPointCloud(object.uuid,object.scale, object.position, object.points, object.color, object.size)
          }
        })
        
        // Now Accept New Objects
        this.sit()
      })


    }

    /////////////////////////////////
    //// DEFINE LISTENING EVENTS ////
    /////////////////////////////////
    async sit(){
      console.log("Waiting on events..")

      // Kill Event
      this.socket.on("kill", (data)=>{
        window.close()
      })
      
      // Display Objects Event
      this.socket.on("objects", (data)=>{
        console.log("Sever Requested to Display Objects")
        console.log(this.objects)
      })
      // Top Text
      this.socket.on("text", (data)=> {
        document.getElementById("info").innerText = data.text
        document.getElementById("info").style.visibility = "visible"

        setTimeout(()=>{
          document.getElementById("info").style.visibility = "hidden"

        },data.time)
      })

      // Box Event
      this.socket.on("box", (data)=>{
        console.log(`Box Event of Type ${data.event}`)
        if(data.event == "add"){
          this.addBox(data.uuid, data.scale, data.position, data.color)
        } else if (data.event == "remove"){
          this.objects.forEach((box, index)=>{
            if (box.uuid == data.uuid){
              this.remove(index)
              return
            }
          })
        } else if (data.event == 'move'){
          this.objects.forEach((box, index)=>{
            if (box.uuid == data.uuid){
              this.objects[index].move(data.position.x, data.position.y, data.position.z )
              return
            }
          })
        }
        
      })

      // Point CLoud Event
      this.socket.on("point", (data)=>{
        console.log(`Point Cloud Event of Type ${data.event}`)
        if(data.event == "add"){
          this.addPointCloud(data.uuid, data.scale, data.position, data.points, data.color, data.size)
        } else if (data.event == "remove"){
          this.objects.forEach((pc, index)=>{
            if (pc.uuid == data.uuid){
              this.remove(index)
              return
            }
          })
        } else if (data.event == 'move'){
          console.log("MOVING SLKDJFKLSJDF")
          this.objects.forEach((pc, index)=>{
            if (pc.uuid == data.uuid){
              this.objects[index].move(data.position.x, data.position.y, data.position.z )
              return
            }
          })
        } else {
          console.log("Uncaught Event of type " + data.event + " with UUID " + data.uuid)
        }
        
      })
      

    }
    //////////////////////////////
    //// Wrapper Class Events ////
    //////////////////////////////
    addBox(uuid, scale, position, color){
      let box = new Box(this.scene, uuid, scale, position, color )
      this.objects.push(box)
      return box
    }
    remove(index){
      if(this.objects.length > 0){
        this.objects[index].remove()
        return this.objects.splice(index, 1)[0]
        
      }else{
        console.error("Tried to remove item but object.length is already gone")
        return
      }
    }
    
    addPointCloud(uuid, scale, position, points, color, size){
      let _points = new Points(this.scene, uuid, points, {scale, position, points, color, size})
      console.log(_points)
      this.objects.push(_points)
      return _points
    }



}

