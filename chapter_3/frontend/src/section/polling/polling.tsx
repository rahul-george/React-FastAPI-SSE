import { useState } from "react";
import { Button, Box, Heading } from "@chakra-ui/react";
import api from "@/lib/axios";

function Polling() {
  const [message, setMessage] = useState("Loading...");

  const handleFetch = async () => {
    try {
      const response = await api.get("/polling/logs/1");
      setMessage(JSON.stringify(response.data, null, 2));
      //setMessage(JSON.parse(response.data))
      console.log("✅ Data:", response.data);
    } catch (error) {
      console.error("❌ Error fetching data:", error);
      setMessage("Error fetching data");
    }
  };

  return (
    <Box p={6}>
      <Heading mb={4}>Polling Approach</Heading>
      <Button colorScheme="teal" onClick={handleFetch}>
        Get next commentary
      </Button>
      <Box mt={4} p={4} bg="red.500" borderRadius="md">
        API Response: {message}
      </Box>
    </Box>
  );
}

export default Polling;
