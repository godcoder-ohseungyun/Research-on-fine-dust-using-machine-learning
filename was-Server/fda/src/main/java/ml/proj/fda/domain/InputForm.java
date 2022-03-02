package ml.proj.fda.domain;

public class InputForm {

    private String city;
    private String district;
    private int size; //집 평수

    public InputForm(String city, String district, int size) {
        this.city = city;
        this.district = district;
        this.size = size;
    }
}
