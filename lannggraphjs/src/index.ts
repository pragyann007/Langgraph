    // imports

    import {StateGraph,Annotation,messagesStateReducer, Graph, START, END} from "@langchain/langgraph"
    import { registry } from "zod"
    import { no } from "zod/v4/locales"

    // define state
    export const MyState = Annotation.Root({
        vala:Annotation<string>(),
        valb:Annotation<string>()
    })

    // define node function
    function nodeA(state:typeof MyState.State){
        return {vala:"a"} ; 

        
    }


    function nodeB (state:typeof MyState.State){
        return {valb:"b"} ; 
    }

    const graph = new StateGraph(MyState)
    .addNode("nodea",nodeA)
    .addNode("nodeb",nodeB)
    .addEdge(START,"nodea")
    .addEdge("nodea","nodeb")
    .addEdge("nodeb",END)


    const workflow = graph.compile()


    async function run (){
        const results = await workflow.invoke({vala:"",valb:""}    )
        console.log(results)
    }
    run()


  



    // define graph

    // add nodes

    // add edges

    // compile

    // exeucte invoke()