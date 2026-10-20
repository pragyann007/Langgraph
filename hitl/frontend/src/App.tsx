import React, { useState } from 'react'
import axios from "axios"
interface DataVal{
  thread_id:string
  message:string
}

const App = () => {
  const [dataVal,setDataVal]=useState<DataVal|null>()
  const [approval,setApproval]=useState<"yes"|"no">()

  const mockOrders = [
    {
      id:1,
      items: "Wireless Ergonomic Mouse, Mechanical Keyboard",
      price: "129.98",
      processed: true,
      final_msg: "Order payment confirmed. Items packed and handed to carrier.",
      o_type: "pay"
    },
    {
      id:2,

      items: "Return Request: Leather Jacket (Size M)",
      price: "0.00",
      processed: true,
      final_msg: "Return label generated and sent to customer email.",
      o_type: "general"
    },
    {
      id:3,

      items: "4K Ultra HD Monitor 27-inch",
      price: "349.99",
      processed: false,
      final_msg: "Awaiting payment verification from bank.",
      o_type: "pay"
    },
    {
      id:4,

      items: "Customer Support Query: Size chart guidance",
      price: "0.00",
      processed: false,
      final_msg: "Assigned to support agent. Pending response.",
      o_type: "general"
    },
    {
      id:5,

      items: "Noise-Canceling Headphones, USB-C Cable (2-Pack)",
      price: "199.50",
      processed: true,
      final_msg: "Transaction successful. Order delivered.",
      o_type: "pay"
    }
  ];
  const handleWorkflow = async (id) => {

    const datas = mockOrders.find((i)=>i.id==id)
    const res = await axios.post("http://localhost:8000/ai/start", datas)
    const dataVal = res?.data
    setDataVal(dataVal)
    console.log(dataVal)
  }

  const handleUserApproval = async(decison)=>{

    const res  = await axios.post(`http://localhost:8000/ai/approve/${dataVal.thread_id}`,{decison})
    const data = res.data 
    console.log(data)
   

  }

  
  return (
    <div>
      <h1>Hiii</h1>

      <div className='flex gap-18 justify-center items-center' >
        {mockOrders.map((elem, indx) => (
          <div key={indx} className='w-70 mb-40 h-60  bg-red-300 rounded-2xl ' >
            <div className='p-4 ' >
              <h1>{elem.items}</h1>
              <h2>{elem.price}</h2>
              <h3>Processed : <span>{elem.processed ? "Processed" : "Not Processed"}</span></h3>
              <h4>{elem.o_type}</h4>
              <button className='bg-white text-black text-xl cursor-pointer p-2 mt-10 rounded-md' onClick={()=>handleWorkflow(elem.id)} > Start the workflow </button>


            </div>
          </div>
        ))}
      </div>

      <div>
        {dataVal ? <div className='w-80 h-20 bg-white ' >
          <h2>{dataVal.message}</h2>
          <div>
            <button className='bg-green text-white text-xl cursor-pointer p-2 mt-10 rounded-md' onClick={()=>handleUserApproval("yes")} >YES</button>
            <button className='bg-red text-white text-xl cursor-pointer p-2 mt-10 rounded-md'  onCanPlay={()=>handleUserApproval("no")} >NO</button>
          </div>
        </div>:<div></div>}
      </div>

    </div>
  )
}

export default App