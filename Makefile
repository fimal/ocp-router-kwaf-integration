haproxy-ocp-extauth:
	# install sample apps and haproxy route
	helm install haproxy-sample -n test --create-namespace sample-haproxy-integration --wait --timeout

	# install kwaf in ext-authz mode (central)
	#make KIND_WAIT=10m MORE="-f sample-haproxy-integration/_authz-poc.yaml -f tests/openshift.yaml --set waas-controller.userIpHeaders=x-cdn" install	
	kubectl apply -n kwaf -f sample-haproxy-integration/templates/_profile.yaml

	# install spoa (Stream Processing Offload Engine) https://www.haproxy.com/blog/extending-haproxy-with-the-stream-processing-offload-engine/
	kubectl apply -n kwaf -f sample-haproxy-integration/templates/_waas-spoa-deployment.yaml
	kubectl apply -n kwaf -f sample-haproxy-integration/templates/_waas-spoa-service.yaml

	kubectl scale --replicas 0 -n openshift-cluster-version deployments/cluster-version-operator
	kubectl scale --replicas 0 -n openshift-ingress-operator deployments ingress-operator
	kubectl -n openshift-ingress scale deployment --replicas=0 router-default
	kubectl patch -n openshift-ingress deployment router-default  --patch-file sample-haproxy-integration/templates/_volumes.json
	kubectl -n openshift-ingress scale deployment --replicas=1 router-default

haproxy-ocp-extauth-clear:
	kubectl scale --replicas 1 -n openshift-cluster-version deployments/cluster-version-operator
	kubectl scale --replicas 1 -n openshift-ingress-operator deployments ingress-operator
	helm delete -n test haproxy-sample
	kubectl delete -n kwaf svc waas-spoa-service
	kubectl delete -n kwaf deployment waas-spoa-deployment