FROM skhatiri/aerialist:latest
RUN pip3 install -e /src/aerialist/

COPY ./requirements.txt /src/DeepHyperion/requirements.txt
WORKDIR /src/DeepHyperion/
RUN pip3 install -r /src/DeepHyperion/requirements.txt

COPY ./ /src/DeepHyperion/
RUN mkdir -p ./logs/ ./results/ ./generated_tests/

ENV AGENT local
ENV AVOIDANCE_LAUNCH /src/aerialist/aerialist/resources/simulation/collision_prevention.launch
ENV AVOIDANCE_BOX /src/aerialist/aerialist/resources/simulation/box.xacro
