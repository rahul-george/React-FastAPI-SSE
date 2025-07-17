

# React-FastAPI-SSE

Proof of concept on how to implement SSE using FastAPI and how to consume SSE endpoints in React

# Chapters

chapter 1 - normal fastapi endpoint with profiler
chapter 2 - added a react application to consume the endpoint in a polled manner
chapter 3 - implemented an SSE endpoint + React application section to consume the SSE endpoint

## Future
1. Connecting with mongodb streams 
2. Pub-Sub example with POST and SSE GET
3. SSE for POST endpoints. 

# About SSE
1. Unidirectional stream 
2. Textual streams
3. Reduced requests
4. Browser support not available for older browsers


# Issues
1. When testing on github codespaces, the stream terminates at 60 seconds. 

    1.1 Expecting this to be a limit put by the reverse proxy or by github codespaces. 

2. **[Fixed]** At the end of the message stream an error is raised. 

    **Solution:** Resolved after creating a named event listener on the event source to listen for events with type 'Completed' and then closing the event source. 

3. How to send custom headers and authentication with eventSource API? 

4. **[Fixed]** Tried a reconnection fix, but it is treating it as a new request and not sending remaining data but starting from scratch. 

    **Solution:** Resolved after creating a named event listener on the event source to listen for events with type 'Completed' and then closing the event source. 


## Run in codespaces or local

For local execution, additionally set up python and node. 

Setup backend

```bash
    cd chapter_x/
    cd frontend/
    pip install requirements.txt
```


Start the backend

```bash
  cd chapter_x/
  cd backend/
  fastapi dev main.py
```

Setup frontend

```bash
    cd chapter_x/
    cd frontend/
    npm install
```

Start frontend server

```bash
  npm run start
```


References: 
1. https://dev.to/lagoni/how-to-implement-eventsource-and-sse-in-your-frontend-and-backend-18co
2. https://fastapi.tiangolo.com/advanced/custom-response/#streamingresponse
3. https://blog.logrocket.com/using-fetch-event-source-server-sent-events-react/


