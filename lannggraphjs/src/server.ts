import express from "express"
import dotenv from "dotenv"

dotenv.config()
import mongoose  from "mongoose";
import { runAgent } from "./agent";


const connectDb = async()=>{
    try {
        await mongoose.connect(process.env.MONGO_URI!);
        console.log("Mongo db connected ")

        return true 
        
    } catch (error) {
        
        console.log("MOngo db failed.")
        throw error
        
    }

}
connectDb()

const port = process.env.PORT || 8080 ;

const app = express();

app.use(express.json());

app.get("/",(req,res)=>{
    res.status(200).json({message:"Healthy"})
})



app.post("/chatbot/chat",async(req,res)=>{

    const {query} = req.body;

    const results = await runAgent(query);
    return res.status(200).json({message:"success",results});


})

app.listen(port,()=>{

    console.log("Server is running at port ",port);
})

