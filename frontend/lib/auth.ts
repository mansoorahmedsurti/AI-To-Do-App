import { createAuthClient } from 'better-auth/react';

export const authClient = createAuthClient({
  baseURL: process.env.NEXT_PUBLIC_AUTH_URL || 'http://localhost:3000',
});

// Define a type for the session
export interface Session {
  user: {
    id: string;
    email: string;
    emailVerified: boolean;
    name: string;
    createdAt: Date;
    updatedAt: Date;
    image?: string;
  };
  session: {
    id: string;
    userId: string;
    expiresAt: Date;
    ipAddress?: string;
    userAgent?: string;
  };
}

// Sign in/out types - using fetch API directly
export interface AuthResponse {
  data?: {
    session: {
      id: string;
      userId: string;
      expiresAt: Date;
    };
    user: {
      id: string;
      email: string;
      name: string;
    };
  };
  error?: {
    message: string;
  };
}
