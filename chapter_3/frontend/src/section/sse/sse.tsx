import React, { useRef, useEffect, useState } from "react";
import { Box, Button, Heading } from "@chakra-ui/react";

function ServerSentEvents() {
  const [events, setEvents] = useState([]);

  const eventSourceRef = useRef<EventSource | null>(null);
  const reconnectTimerRef = useRef<NodeJS.Timeout | null>(null);

  useEffect(() => {
    const connect = () => {
      const eventSource = new EventSource(
        "https://bug-free-orbit-9q6p79wx6v92xrg5-8000.app.github.dev/sse/logs/simple"
      );
      // const eventSource = new EventSource("https://bug-free-orbit-9q6p79wx6v92xrg5-8000.app.github.dev/sse/logs/commentary");

      eventSourceRef.current = eventSource;
      eventSource.onmessage = (event) => {
        // console.log(event)
        if (event.type == "Completed") {
          console.log("Closing event source");
          eventSource.close();
        }
        const newEvent = JSON.parse(event.data);
        setEvents((prevEvents) => [newEvent, ...prevEvents]);
      };

      eventSource.onerror = (error) => {
        console.log(error);
        console.error("SSE connection error");
        eventSource.close();

        // Retry after delay
        reconnectTimerRef.current = setTimeout(connect, 3000);
      };
    };

      connect();

      return () => {
        console.log("Cleaning up SSE connection");
        eventSourceRef.current?.close();
        if (reconnectTimerRef.current) {
          clearTimeout(reconnectTimerRef.current);
        }
      };
  }, []);

  return (
    <Box p={6}>
      <Heading mb={4}>Server Sent Events Approach</Heading>
      <Button colorScheme="teal">Start Commentary update</Button>
      {events.map((event) => (
        <Box mt={4} p={4} bg="red.500" borderRadius="md">
          API Response: {event}
        </Box>
      ))}
    </Box>
  );
}

export default ServerSentEvents;
