package com.soa.lab8;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@SpringBootApplication
@RestController
public class TerraformApp {

    public static void main(String[] args) {
        SpringApplication.run(TerraformApp.class, args);
    }

    @GetMapping("/terraform")
    public String terraform() {
        return "Infrastructure Provisioning using Terraform : Executed";
    }
}
