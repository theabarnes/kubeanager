#!/home/opal/myenv/bin/python3
import sys
import subprocess

appname=sys.argv[1]
port=sys.argv[2]
namespace=sys.argv[3]
certdomain=sys.argv[4]

text="""apiVersion: v1
kind: Service
metadata:
  name: {appname}-svc
spec:
  ports:
  - name: http
    port: 80
    targetPort: {port}
  - name: https
    port: 443
    targetPort: {port}
  selector:
    app: {appname}
---
apiVersion: extensions/v1beta1
kind: Ingress
metadata:
  name: {appname}-tls
  namespace: $namespace
  annotations:
    kubernetes.io/ingress.class: "nginx"
    cert-manager.io/clusterissuer: "letsencrypt"
spec:
  tls:
  - hosts:
    - {certdomain}
    secretName: {appname}-secret
  rules:
  - host: {certdomain}
    http:
      paths:
      - path: /
        backend:
          serviceName: {appname}
          servicePort: 443"""

print(text.format(appname=appname, port=port))

textout = sys.stdout

with open(appname + '-svc.yaml', 'w') as f:
    sys.stdout = f
    print(text.format(appname=appname, port=port))
    sys.stdout = textout

createingress=subprocess.Popen(["/usr/local/bin/kubectl", "apply", "-f", appname + "-svc.yaml"], stdout=subprocess.PIPE)
CREATEINGRESS=createcluster.stdout.read().strip()
print CREATEINGRESS
