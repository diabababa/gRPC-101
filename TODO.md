
Must have:
TODO: maybe whole workshop should be on docker
TODO: add proto to library


# TODO: do we delete exercices: testing and perfromance

TODO: jaki test locusta moglby pokazac najlepiej przewage nad restem?
Najlepsza demonstracja to bezpośrednie porównanie gRPC vs REST przy tym samym workloadzie. Różnica jest najbardziej widoczna w dwóch miejscach:
1. Wysoka concurrency (HTTP/2 multiplexing vs HTTP/1.1)
gRPC używa HTTP/2 — wiele requestów leci przez jedno połączenie TCP równolegle. REST (HTTP/1.1) otwiera nowe połączenie per request lub trzyma pool. Przy 100+ userach różnica w latencji i RPS jest wyraźna.

Plan testu: dodać do projektu prosty REST serwer (FastAPI) z identycznym endpointem POST /messages, potem locustfile z dwoma klasami użytkowników:


class GrpcUser(...)   # obecny
class RestUser(HttpUser):  # nowy, ten sam workload przez HTTP/1.1
    @task
    def send_message(self):
        self.client.post("/messages", json={...})
2. Streaming vs polling
GetHistory jako server streaming vs symulowane odpytywanie REST co 500ms — pokazuje przewagę przy danych real-time.


Co byłoby najlepszym demo dla warsztatu?
Polecam opcję 1 (gRPC vs REST) bo:

Liczby mówią same za siebie (widoczna różnica ~2-5x w RPS przy 100+ userach)
Uczestnicy rozumieją REST — kontrast jest intuicyjny
Wymaga tylko dodania FastAPI servera (~20 linii) i nowej klasy w locustfile
Chcesz, żebym to zaimplementował? Potrzebny byłby:

Prosty FastAPI wrapper na istniejący chat service
Rozszerzony locustfile z RestUser obok GrpcUser
Nowy task poe do odpalenia obu serwerów jednocześnie
Authentication and Security in gRPC Microservices - Jan Tattermusch, Google
https://www.youtube.com/watch?v=_y-lzjdVEf0
# TODO: check security https://www.youtube.com/watch?v=zWmGTMBCBVU
# monitoring, live example
# TODO: 5 zadanie ADAM CHECK STREAMING EXAMPLE how it working  
Good to have
TODO: expalin Stub
TODO: dlaczego inaczje wyglada solution z example? wytlumacz Exercise 1
TODO: how genereators works in python ?
TODO: jak dzialja ThredPoolExecutor in python? jak dzialaj Threads in pythopn
How long will take the presentation Introduction? 
TODO: check it Deadline & cancelalation built in?
TODO: pokazac przykald  rest + websockets 
TODO: check it Deadline & cancelalation built in?
TODO: pokazac przykald  rest + websockets 
moze za duzo slajdow na poczatek za malo praktyki ?
Exercies 1 and 2 maybe add little challange? 
czym sie rozni poe od makefile? moze przygotrujemy za pomoca czatyu uzycie komendow make makefile

TODO: Automatization go for each exercise and check if it's working
czym sie rozni poe od makefile? moze przygotrujemy za pomoca czatyu uzycie komendow make makefile

TODO: Automatization go for each exercise and check if it's working
TODO: add link to slides https://marketplace.visualstudio.com/items?itemName=bufbuild.vscode-buf
TODO: co to message {google.protobuf.Struct google.protobuf.Timestamp google.protobuf.Empty}
TODO: co to message Element {reserved 2; reserved "properties"}
TODO: co to typ oneof, optional
Message może być w message'u
option jave_multiple_files
TODO: co to etcd
TODO: co to py-grpc-prometheus
TODO: co to grpcio-health-checking
TODO: co to protobuf
TODO: co to