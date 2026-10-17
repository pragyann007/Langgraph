import {tool} from "@langchain/core/tools"
import { ITicket } from "./tickets.model"
import { createTicket } from "./services";
import {z} from  "zod"

// Define Zod versions of your custom types/enums so the LLM knows the allowed options
const TicketStatusSchema = z.enum(["open", "in_progress", "resolved", "closed"]);
const TicketPrioritySchema = z.enum(["low", "medium", "high", "critical"]);
const TicketCategorySchema = z.enum(["technical", "billing", "general", "bug"]);
const TicketChannelSchema = z.enum(["web", "email", "chat", "api"]);

// Replicate the ITicket interface properties
export const ITicketSchema = z.object({
  title: z.string().describe("A short, descriptive summary of the issue."),
  description: z.string().describe("Detailed description of the user's problem or request."),
  status: TicketStatusSchema.describe("The current operational state of the ticket."),
  priority: TicketPrioritySchema.describe("How urgently this ticket needs to be addressed."),
  category: TicketCategorySchema.describe("The department or topic area this issue belongs to."),
  channel: TicketChannelSchema.describe("The medium through which the ticket originated."),
});



const createTicketHandler = async ({data}:{data:ITicket}): Promise<any> => {
    // Add your logic to handle ticket creation here
    const d = await createTicket(data);

    return d; // Replace with actual implementation
};


export const createTicketTool = tool(
    createTicketHandler,
    { name: "createTicket",description:"Thi stool is used to create a new ticket entry in db",schema:z.object({data:ITicketSchema})}
);