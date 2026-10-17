import { ITicket, Ticket } from "./tickets.model";

export const createTicket = async(ticket:ITicket)=>{
try {
        const create = await Ticket.create(ticket);
    
        return {message:"Created sucessfully!",data:create}
} catch (error) {
    console.log(error)
    throw  error

    
}



}