import NextAuth from 'next-auth';
import CredentialsProvider from 'next-auth/providers/credentials';

// For now, using a simple credentials provider for demo purposes
// In a real application, you would connect to a database or external service
const handler = NextAuth({
  providers: [
    CredentialsProvider({
      name: 'Credentials',
      credentials: {
        email: { label: 'Email', type: 'email' },
        password: { label: 'Password', type: 'password' }
      },
      async authorize(credentials) {
        // This is a simplified example - in a real app, you would validate against a database
        if (!credentials?.email || !credentials?.password) {
          return null;
        }

        // Placeholder validation - replace with actual user validation
        // This is just for demonstration purposes
        if (credentials.email && credentials.password) {
          return {
            id: '1',
            email: credentials.email,
            name: credentials.email.split('@')[0] // Simple name extraction
          };
        }

        return null;
      }
    })
  ],
  pages: {
    signIn: '/login', // Custom login page
  },
  callbacks: {
    async jwt({ token, user }) {
      if (user) {
        token.id = user.id;
      }
      return token;
    },
    async session({ session, token }) {
      if (token) {
        session.user.id = token.id as string;
      }
      return session;
    }
  },
  secret: process.env.NEXTAUTH_SECRET || 'fallback-test-secret',
  session: {
    strategy: 'jwt',
    maxAge: 24 * 60 * 60, // 24 hours
  }
});

export { handler as GET, handler as POST };