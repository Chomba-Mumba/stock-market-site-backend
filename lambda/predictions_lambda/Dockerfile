FROM public.ecr.aws/lambda/python:3.9

# Copy function code and dependencies
COPY predictions.py ./
COPY utils/ ./utils/

COPY requirements.txt ./

#Install requirements
RUN python -m pip install -r requirements.txt

CMD [ "predictions.lambda_handler" ]