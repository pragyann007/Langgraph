import {createAgent} from "langchain"
import {ChatGoogle} from "@langchain/google"
import { createTicketTool, ITicketSchema } from "./tools"
import dotenv from "dotenv"
dotenv.config()


const llm  = new ChatGoogle({model:"gemini-2.5-flash"})

const agent = createAgent({
    model:llm,
    tools:[createTicketTool],
    systemPrompt:"You are helful agent to understand users ticket and auto add it in databsse using createTicketTool after sucefully creating the stuff send the ticket id to te user so that they can taka refernce and ask to other staffs. font ask anything to user when user says their query just analyse and add according to yor mentality or brilliancy cause people can add high priority for very low prioroty task too so when user give some query just analyse and base on your understanding work it",
})

export const runAgent = async(query:string)=>{
    const results = await agent.invoke({
        messages:[{role:"user",content:query}]
    })

    console.log(results.messages[results.messages.length-1]);

    return {result:results.messages[results.messages.length-1]}

    
}
