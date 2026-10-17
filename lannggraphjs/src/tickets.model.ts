// models/Ticket.ts
import { Schema, model, Document } from 'mongoose';

// types/ticket.ts

export enum TicketStatus {
    OPEN = 'open',
    IN_PROGRESS = 'in_progress',
    PENDING_CUSTOMER = 'pending_customer',
    RESOLVED = 'resolved',
    CLOSED = 'closed'
  }
  
  export enum TicketPriority {
    LOW = 'low',
    MEDIUM = 'medium',
    HIGH = 'high',
    URGENT = 'urgent'
  }
  
  export enum TicketCategory {
    TECHNICAL = 'technical',
    BILLING = 'billing',
    ACCOUNT = 'account',
    FEATURE_REQUEST = 'feature_request',
    OTHER = 'other'
  }
  
  export enum TicketChannel {
    WEB_PORTAL = 'web_portal',
    EMAIL = 'email',
    CHAT = 'chat',
    PHONE = 'phone'
  }
  
export interface ITicket  {
  title: string;
  description: string;
  status: TicketStatus;
  priority: TicketPriority;
  category: TicketCategory;
  channel: TicketChannel;
}

const ticketSchema = new Schema<ITicket>({
  title: { 
    type: String, 
    required: true, 
    trim: true 
  },
  description: { 
    type: String, 
    required: true 
  },
  status: {
    type: String,
    enum: Object.values(TicketStatus),
    default: TicketStatus.OPEN,
    required: true
  },
  priority: {
    type: String,
    enum: Object.values(TicketPriority),
    default: TicketPriority.MEDIUM,
    required: true
  },
  category: {
    type: String,
    enum: Object.values(TicketCategory),
    default: TicketCategory.OTHER,
    required: true
  },
  channel: {
    type: String,
    enum: Object.values(TicketChannel),
    default: TicketChannel.WEB_PORTAL,
    required: true
  },

 
}, { timestamps: true });

export const Ticket = model<ITicket>('Ticket', ticketSchema);
