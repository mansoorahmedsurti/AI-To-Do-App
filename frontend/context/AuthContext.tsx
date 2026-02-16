'use client';

import React, { createContext, useContext, useEffect, useState, ReactNode } from 'react';
import { signIn as nextSignIn, signOut as nextSignOut, useSession } from 'next-auth/react';

interface User {
  id: string;
  email: string;
}

interface AuthContextType {
  user: User | null;
  signIn: (credentials: { email: string; password: string }) => Promise<void>;
  signUp: (credentials: { email: string; password: string }) => Promise<void>;
  signOut: () => Promise<void>;
  isLoading: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const { data: session, status } = useSession();
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    if (status === 'loading') {
      setIsLoading(true);
    } else {
      setIsLoading(false);
      if (session?.user) {
        setUser({
          id: session.user.email || 'unknown',
          email: session.user.email || '',
        });
      } else {
        setUser(null);
      }
    }
  }, [session, status]);

  const signIn = async ({ email, password }: { email: string; password: string }) => {
    try {
      // First, authenticate with the backend to get the access token
      const backendResponse = await fetch('http://localhost:8000/auth/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
      });

      if (!backendResponse.ok) {
        const errorData = await backendResponse.json();
        throw new Error(errorData.detail || 'Backend authentication failed');
      }

      const backendData = await backendResponse.json();
      
      // Store the backend token
      if (backendData.access_token) {
        localStorage.setItem('backend_access_token', backendData.access_token);
      }

      // Then authenticate with NextAuth
      const result = await nextSignIn('credentials', {
        email,
        password,
        redirect: false,
      });

      if (result?.ok) {
        // User is authenticated, the session will update automatically
        console.log('Sign in successful');
      } else {
        throw new Error(result?.error || 'Sign in failed');
      }
    } catch (error) {
      console.error('Sign in error:', error);
      throw error;
    }
  };

  const signUp = async ({ email, password }: { email: string; password: string }) => {
    try {
      // Call the backend API for registration
      const response = await fetch('http://localhost:8000/auth/register', {  // Updated to backend URL
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Registration failed');
      }

      const data = await response.json();

      // Store the token in localStorage or sessionStorage
      if (data.access_token) {
        // Store the backend token in localStorage so the API client can access it
        localStorage.setItem('backend_access_token', data.access_token);
        
        // For NextAuth, we typically don't manually handle tokens
        // Instead, we'll trigger the signIn after successful registration
        await signIn('credentials', {
          email,
          password,
          redirect: false,
        });
      }
    } catch (error) {
      console.error('Sign up error:', error);
      throw error;
    }
  };

  const signOut = async () => {
    try {
      // Remove the backend token from localStorage
      if (typeof window !== 'undefined') {
        localStorage.removeItem('backend_access_token');
      }
      
      await nextSignOut({ redirect: false });
    } catch (error) {
      console.error('Sign out error:', error);
      throw error;
    }
  };

  const value = {
    user,
    signIn,
    signUp,
    signOut,
    isLoading,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}