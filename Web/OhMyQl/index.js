const express = require('express');
const cors = require('cors');
const { graphqlHTTP } = require('express-graphql');
const { GraphQLSchema, GraphQLObjectType, GraphQLString } = require('graphql');
const jwt = require('jsonwebtoken');
const path = require('path');
const db = require('./database');
const { JWT_SECRET, PORT, FLAG } = require('./config');

const app = express();
app.use(cors());
app.use(express.static(path.join(__dirname, 'public')));

// Landing page
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// Context middleware — places decoded JWT & db on req.context
const contextMiddleware = (req, res, next) => {
  const token = req.headers.authorization || '';
  let user = null;
  try {
    if (typeof token === 'string' && token.startsWith('Bearer ')) {
      user = jwt.verify(token.replace('Bearer ', ''), JWT_SECRET);
    }
  } catch (e) {
    // ignore, user remains null
  }
  req.context = { user, db };
  next();
};

const errorHandlerMiddleware = (err, req, res, next) => {
  console.error('An error occurred:', err);
  res.status(err.status || 500).json({ 'Error': 'Internal Server Error' });
};

// GraphQL Types
const UserType = new GraphQLObjectType({
  name: 'User',
  fields: {
    username: { type: GraphQLString },
    role: { type: GraphQLString }
  }
});

const AuthResponseType = new GraphQLObjectType({
  name: 'AuthResponse',
  fields: {
    token: { type: GraphQLString }
  }
});

// GraphQL Root Query
const QueryType = new GraphQLObjectType({
  name: 'Query',
  fields: {
    me: {
      type: GraphQLString,
      resolve: async (_, args, context) => {
        const { user, db } = context;
        if (!user) {
          throw new Error('Not authenticated');
        }
        try {
          const userData = await db.getUser(user.username);
          return userData.username;
        } catch (e) {
          throw new Error('User not found');
        }
      }
    },
    getUser: {
      type: GraphQLString,
      args: { username: { type: GraphQLString } },
      resolve: async (_, { username }, context) => {
        const { db } = context;
        try {
          const userData = await db.getUser(username);
          return userData.username;
        } catch (e) {
          throw new Error('User not found');
        }
      }
    }
  }
});

// GraphQL Mutations
const MutationType = new GraphQLObjectType({
  name: 'Mutation',
  fields: {
    login: {
      type: AuthResponseType,
      args: {
        username: { type: GraphQLString },
        password: { type: GraphQLString }
      },
      resolve: async (_, { username, password }, context) => {
        const { db } = context;
        try {
          const user = await db.getUser(username);
          if (!user || user.password !== password) {
            throw new Error('Invalid credentials');
          }
          // IMPORTANT: the token is signed with the *provided* username
          const token = jwt.sign({ username }, JWT_SECRET, { expiresIn: '6m' });
          return { token };
        } catch (e) {
          throw new Error('Authentication failed');
        }
      }
    },
    setFlagOwner: {
      type: GraphQLString,
      args: { username: { type: GraphQLString } },
      resolve: async (_, { username }, context) => {
        const { user } = context;
        if (!user) {
          throw new Error('Not authorized');
        }
        if (user.username !== username) {
          throw new Error('You can only set flag for your own account');
        }
        try {
          const token = jwt.sign({ username, flagOwner: true }, JWT_SECRET, { expiresIn: '6m' });
          return token;
        } catch (e) {
          throw new Error('Token generation failed');
        }
      }
    }
  }
});

const schema = new GraphQLSchema({
  query: QueryType,
  mutation: MutationType
});

// Mount GraphQL (with request-specific context)
app.use('/graphql', contextMiddleware, graphqlHTTP((req) => ({
  schema,
  graphiql: false,
  context: req.context,
  pretty: false
})));

// Admin route -> returns the flag if token has flagOwner=true
app.get('/admin', (req, res) => {
  const token = req.headers.authorization;
  let user;
  try {
    if (token && token.startsWith('Bearer ')) {
      user = jwt.verify(token.replace('Bearer ', ''), JWT_SECRET);
    }
  } catch (e) {
    return res.status(403).send('Forbidden');
  }
  if (!user || user.flagOwner !== true) {
    return res.status(403).send('Forbidden');
  }
  res.type('text/plain').send(FLAG);
});

app.use(errorHandlerMiddleware);

app.listen(PORT, () => {
  console.log(`CYBERDUNE OhMyQL server on port ${PORT}`);
});
