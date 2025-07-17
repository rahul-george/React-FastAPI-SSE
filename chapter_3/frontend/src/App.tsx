import { Box, Separator} from "@chakra-ui/react";

import Polling from "@/section/polling/polling";
import ServerSentEvents from "@/section/sse/sse";

function App() {

  return (
    <Box p={6}>
      <Polling></Polling>
      <Separator></Separator>
      <ServerSentEvents></ServerSentEvents>
    </Box>
  );
}

export default App;
