import { Box, Separator} from "@chakra-ui/react";

import Polling from "@/section/polling/polling";

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
      <Polling></Polling>
    </Box>
  );
}

export default App;
