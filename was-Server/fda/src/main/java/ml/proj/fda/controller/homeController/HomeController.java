package ml.proj.fda.controller.homeController;


import lombok.extern.slf4j.Slf4j;
import ml.proj.fda.domain.Analysis;
import ml.proj.fda.domain.InputForm;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.core.ParameterizedTypeReference;
import org.springframework.http.*;
import org.springframework.http.converter.HttpMessageConverter;
import org.springframework.http.converter.StringHttpMessageConverter;
import org.springframework.http.converter.json.MappingJackson2HttpMessageConverter;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.ModelAttribute;
import org.springframework.web.bind.annotation.ResponseBody;
import org.springframework.web.client.RestTemplate;
import org.thymeleaf.expression.Lists;

import javax.annotation.PostConstruct;
import java.nio.charset.Charset;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.List;


@Slf4j
@Controller
public class HomeController {

    RestTemplate restTemplate;

    @Autowired
    private HomeController(RestTemplate restTemplate) {
        this.restTemplate = restTemplate;
    }

    @GetMapping
    @ResponseBody
    public List<Analysis> getHome() {
        log.info("api ok");
        return helloMachineLearning();
    }

    //https://luvstudy.tistory.com/52
    //restTemplate 리스트 형태로 받기
    private List<Analysis> helloMachineLearning() {

        HttpEntity<String> entity = makeEntity();

        //ResponseEntity<List<Analysis>> response = restTemplate.exchange("http://127.0.0.1:5000/api/result", HttpMethod.GET, null, new ParameterizedTypeReference<List<Analysis>>() {});
        ResponseEntity<List<Analysis>> response = restTemplate.exchange("http://127.0.0.1:5000/test", HttpMethod.GET, entity , new ParameterizedTypeReference<List<Analysis>>() {
        });
        List<Analysis> list = response.getBody();


        return list;
    }


    private HttpEntity<String> makeEntity() {
        HttpHeaders headers = new HttpHeaders();

        Charset utf8 = Charset.forName("UTF-8");

        MediaType mediaType = new MediaType("application", "json", utf8);

        headers.setContentType(mediaType);

        HttpEntity<String> entity = new HttpEntity<String>("hello api server", headers);

        return entity;
    }

    @PostConstruct
    private void RestTemplateConverterSetting() {

        System.out.println("RestTemplate setting..");
        restTemplate.getMessageConverters().add(0,new StringHttpMessageConverter(Charset.forName("UTF-8")));

    }
}
