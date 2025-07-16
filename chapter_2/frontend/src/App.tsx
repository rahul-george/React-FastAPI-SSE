import { useEffect, useState } from "react";
import { Button, Box, Heading } from "@chakra-ui/react";
import api from "@/lib/axios";

function App() {
  const [message, setMessage] = useState("Loading...");

const handleFetch = async () => {
    try {
      const response = await api.get('/polling/logs/1');
      setMessage(JSON.stringify(response.data, null, 2));
      console.log('✅ Data:', response.data);
    } catch (error) {
      console.error('❌ Error fetching data:', error);
      setMessage('Error fetching data');
    }
  };

  return (
    <Box p={6}>
      <Heading mb={4}>Hello Chakra UI 👋</Heading>
      <Button colorScheme="teal" onClick={handleFetch}>Click Me</Button>
      <Box mt={4} p={4} bg="red.500" borderRadius="md">
        API Response: {message}
      </Box>
    </Box>
  );
}

export default App;
