// See https://aka.ms/new-console-template for more information
using System.Net;
using System.Net.Sockets;




public class StaticSingleton {
    public static SampleMoveAroundDrone sampleMoveAroundDrone;
    public static DroneSoccerXrByteListener droneSoccerXrByteListener;

}


public class Program {

    public static void Main(string[] args)
    {
        StaticSingleton.sampleMoveAroundDrone = new SampleMoveAroundDrone();
        Thread threadLogic = new Thread(StaticSingleton.sampleMoveAroundDrone.StartLogicThread);
        threadLogic.Start();

        StaticSingleton. droneSoccerXrByteListener = new DroneSoccerXrByteListener("127.0.0.1", 2571);
        Thread threadListen = new Thread(StaticSingleton.droneSoccerXrByteListener.Listen);
        threadListen.Start();


        while (true)
        {
            Thread.Sleep(1000);
            DisplayGameState();
        }

        void DisplayGameState()
        {

            int playerIndex = 0;
            DroneSoccerPosition player = StaticSingleton.droneSoccerXrByteListener.m_dronesPosition[playerIndex];

            Console.WriteLine($"F:{StaticSingleton.droneSoccerXrByteListener.m_serverPositionPushedFrame}" +
                $" Drone {player.m_x}, {player.m_y}, {player.m_z}, {player.m_eulerY}"
                );

        }

    }
}




public class SampleMoveAroundDrone {

    public PushUdpIntegerToLocalClient client = new PushUdpIntegerToLocalClient("127.0.0.1", 2560);
    public GamepadDroneInput input = new GamepadDroneInput(-1);

    public void StartLogicThread() { 
        while (true)
        {
            int millisecondsBetweenAction = 4000;
            input.SetJoysticks(0.0f, 0.0f, 0.0f, 0.0f);
            PushWait(millisecondsBetweenAction);

            input.SetJoysticks(RandomUtility.R11(), RandomUtility.R11(), RandomUtility.R11(), RandomUtility.R11());
            PushWait(millisecondsBetweenAction);


            input.SetRotateLeft();
            PushWait(millisecondsBetweenAction);
            input.SetRotateRight();
            PushWait(millisecondsBetweenAction);

            input.SetForward();
            PushWait(millisecondsBetweenAction);
            input.SetBackward();
            PushWait(millisecondsBetweenAction);

            input.SetLeft();
            PushWait(millisecondsBetweenAction);
            input.SetRight();
            PushWait(millisecondsBetweenAction);

            input.SetUp();
            PushWait(millisecondsBetweenAction);
            input.SetDown();
            PushWait(millisecondsBetweenAction);


        }
    }

    private void PushWait(int millisecondsBetweenAction)
    {
        PushInput();
        Sleep(millisecondsBetweenAction);
    }

    void Sleep(int millisecondsBetweenAction)
    {
        Thread.Sleep(millisecondsBetweenAction);
    }

    void PushInput() { 
    
        client.SendInteger(input.m_integerRepresentation);
    }

}

public class DroneSoccerPositionCompressed
{
    public int m_index_0_11;
    public int m_droneIndex_1_12;
    public short m_x;
    public short m_y;
    public short m_z;
    public byte m_eulerX;
    public byte m_eulerY;
    public byte m_eulerZ;
}
public class DroneSoccerPosition
{
    public int m_index_0_11;
    public int m_droneIndex_1_12;
    public float m_x;
    public float m_y;
    public float m_z;
    public float m_eulerX;
    public float m_eulerY;
    public float m_eulerZ;
}

public class DroneSoccerXrByteListener {

    public int m_port;
    public string m_ipv4;
    private Socket m_socket;

    public DroneSoccerXrByteListener(string ipv4, int port)
    {
        m_ipv4 = ipv4;
        m_port = port;
        // open socket to ip and port to send udp message
        m_socket = new Socket(AddressFamily.InterNetwork, SocketType.Dgram, ProtocolType.Udp);
        m_socket.Bind(new IPEndPoint(IPAddress.Parse(m_ipv4), m_port));
        for (int i = 0; i < 12; i++)
        {
            m_dronesPosition.Add(new DroneSoccerPosition() { m_index_0_11= i, m_droneIndex_1_12=i+1});
        }
    }

    public List<DroneSoccerPosition> m_dronesPosition = new List<DroneSoccerPosition>();
    public long m_dateTimeserver;
    public long m_serverPositionPushedFrame;

    public void Listen()
    {

        byte[] buffer = new byte[1024];
        while (true)
        {
            int bytesRead = m_socket.Receive(buffer);

            if (bytesRead>9)
            {
                byte droneId = buffer[0];
                if (droneId == 1)
                { 
                    long date = BitConverter.ToInt64(buffer, 1);
                    long frame= BitConverter.ToInt64(buffer, 9);
                    m_dateTimeserver = date;
                    m_serverPositionPushedFrame = frame;

                    for(int i=17, j=0; i<bytesRead; i+=9, j++)
                    {

                        DroneSoccerPosition drone;
                        if (j < m_dronesPosition.Count)
                        {
                            drone = m_dronesPosition[j];
                        }
                        else
                        {
                            drone = new DroneSoccerPosition();
                            m_dronesPosition.Add(drone);
                            m_dronesPosition[j].m_index_0_11 = j;
                            m_dronesPosition[j].m_droneIndex_1_12 = j + 1;
                        }
                        drone.m_x = BitConverter.ToInt16(buffer, i)/ 1000f;
                        drone.m_y = BitConverter.ToInt16(buffer, i+2) / 1000f;
                        drone.m_z = BitConverter.ToInt16(buffer, i+4) / 1000f;
                        drone.m_eulerX = (buffer[i+6] / 255f)*360f;
                        drone.m_eulerY = (buffer[i+7] / 255f)*360f;
                        drone.m_eulerZ = (buffer[i+8] / 255f)*360f;
                    }
                }
            }
        }
    }
    public void Close()
    {
        m_socket.Close();
    }

    ~DroneSoccerXrByteListener()
    {
        Close();
    }
}


public class RandomUtility
{
    public static float R11()
    {
        return (float)(new Random().NextDouble() * 2 - 1);
    }
}


public class GamepadDroneInput {

    public int m_droneId=-1;
    public float m_rotateLeftRight;
    public float m_moveUpDown;
    public float m_moveLeftRight;
    public float m_moveForwardBackward;
    public int m_integerRepresentation;

    public GamepadDroneInput(int droneId)
    {
        m_droneId = droneId;
    }
    public void SetJoysticks(float rotateLeftRight, float moveUpDown, float moveLeftRight, float moveForwardBackward)
    {
        m_rotateLeftRight = rotateLeftRight;
        m_moveUpDown = moveUpDown;
        m_moveLeftRight = moveLeftRight;
        m_moveForwardBackward = moveForwardBackward;       

        bool isNegative = m_droneId<0;
        int cmd = 0;
        cmd+= ConvertPercent11To199(ref m_rotateLeftRight)*1000000;
        cmd+= ConvertPercent11To199(ref m_moveUpDown)*10000;
        cmd+= ConvertPercent11To199(ref m_moveLeftRight)*100;
        cmd+= ConvertPercent11To199(ref m_moveForwardBackward)*1;
        cmd+= Math.Abs(m_droneId)*100000000;
        if(isNegative) {
            cmd *= -1;
        }
        m_integerRepresentation = cmd;
    }


    public int ConvertPercent11To199(ref float percent11) {
        if(percent11==0.0f) {
           return 0;
        } else {
           return  (int)(((percent11+1f)/2f)*98f+1);
        }
    }

    public void SetForward()=>SetJoysticks(0,0,0,1);
    public void SetBackward()=>SetJoysticks(0,0,0,-1);
    public void SetLeft()=>SetJoysticks(0,0,-1,0);
    public void SetRight()=>SetJoysticks(0,0,1,0);
    public void SetUp()=>SetJoysticks(0,1,0,0);
    public void SetDown()=>SetJoysticks(0,-1,0,0);
    public void SetRotateLeft()=>SetJoysticks(-1,0,0,0);
    public void SetRotateRight()=>SetJoysticks(1,0,0,0);
}


public class PushUdpIntegerToLocalClient {

    public int m_port;
    public string m_ipv4;
    private Socket m_socket;

    public PushUdpIntegerToLocalClient(string ipv4, int port)
    {
        m_ipv4 = ipv4;
        m_port = port;
        // open socket to ip and port to send udp message
        m_socket = new Socket(AddressFamily.InterNetwork, SocketType.Dgram, ProtocolType.Udp);
    }

    public void SendInteger(int value)
    {
        byte[] data = BitConverter.GetBytes(value);
        m_socket.SendTo(data, new IPEndPoint(IPAddress.Parse(m_ipv4), m_port));
    }
    public void Close()
    {
        m_socket.Close();
    }
     
    ~PushUdpIntegerToLocalClient()
    {
        Close();
    }
}